from django.contrib import admin

from .models import Entity, EntityText, EntityTime, BotUser


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id']


class EntityTextInlineAdmin(admin.TabularInline):
    model = EntityText
    extra = 1


class EntityTimeInlineAdmin(admin.TabularInline):
    model = EntityTime
    extra = 1


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [EntityTextInlineAdmin, EntityTimeInlineAdmin]
