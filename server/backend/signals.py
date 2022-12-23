from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django_q.tasks import Schedule, schedule

from backend.models import EntityTime


@receiver(post_save, sender=EntityTime)
def entity_time_post_save_handler(instance, created, **kwargs):
    if created:
        for offset in range(-12, 12):
            name = f'entity-time-{instance.id}-offset-{offset}'
            func_name = 'backend.tasks.entity_process'
            args = (instance.id, offset)
            next_run = timezone.now().replace(hour=instance.time.hour,
                                              minute=instance.time.minute)
            next_run -= timezone.timedelta(hours=offset)
            schedule(func_name, *args,
                     name=name,
                     schedule_type=Schedule.DAILY,
                     next_run=next_run)
    else:
        for offset in range(-12, 12):
            name = f'entity-time-{instance.id}-offset-{offset}'
            next_run = timezone.now().replace(hour=instance.time.hour,
                                              minute=instance.time.minute)
            next_run -= timezone.timedelta(hours=offset)
            obj = Schedule.objects.get(name=name)
            obj.next_run = next_run
            obj.save()


@receiver(post_delete, sender=EntityTime)
def entity_time_post_delete_handler(instance, **kwargs):
    for offset in range(-12, 12):
        name = f'entity-time-{instance.id}-offset-{offset}'
        Schedule.objects.filter(name=name).delete()
