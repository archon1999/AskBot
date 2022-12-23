from django.db import models
from ckeditor.fields import RichTextField
from bs4.element import Tag, NavigableString
from bs4 import BeautifulSoup


class Entity(models.Model):
    title = models.CharField(max_length=255,
                             default='',
                             verbose_name='Название')

    class Meta:
        verbose_name = 'Сущность'
        verbose_name_plural = 'Сущности'


class EntityTime(models.Model):
    entity = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='times',
    )
    time = models.TimeField()

    def get_next(self):
        return EntityTime.objects.filter(time__gt=self.time).first()

    def get_prev(self):
        return EntityTime.objects.filter(time__lt=self.time).last()

    class Meta:
        ordering = ['time']


class EntityText(models.Model):
    entity = models.ForeignKey(
        to=Entity,
        on_delete=models.CASCADE,
        related_name='texts',
    )
    text = RichTextField()

    def get_text(self):
        return filter_html(self.text)


def filter_tag(tag: Tag, ol_number=None):
    if isinstance(tag, NavigableString):
        text = tag
        text = text.replace('<', '&#60;')
        text = text.replace('>', '&#62;')
        return text

    html = str()
    li_number = 0
    for child_tag in tag:
        if tag.name == 'ol':
            if child_tag.name == 'li':
                li_number += 1
        else:
            li_number = None

        html += filter_tag(child_tag, li_number)

    format_tags = ['strong', 'em', 'pre', 'b', 'u', 'i', 'code']
    if tag.name in format_tags:
        return f'<{tag.name}>{html}</{tag.name}>'

    if tag.name == 'a':
        return f"""<a href="{tag.get("href")}">{tag.text}</a>"""

    if tag.name == 'li':
        if ol_number:
            return f'{ol_number}. {html}'
        return f'•  {html}'

    if tag.name == 'br':
        html += '\n'

    if tag.name == 'span':
        styles = tag.get_attribute_list('style')
        if 'text-decoration: underline;' in styles:
            return f'<u>{html}</u>'

    if tag.name == 'ol' or tag.name == 'ul':
        return '\n'.join(map(lambda row: f'   {row}', html.split('\n')))

    return html


def filter_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return filter_tag(soup)


class BotUser(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    offset = models.IntegerField(null=True, blank=True)
    ok = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
