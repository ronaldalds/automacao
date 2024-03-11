from django.contrib.admin import ModelAdmin, register
from .models import (
    UserTelegram,
    ApiTelegram,
    BotTelegram,
)


@register(UserTelegram)
class UserTelegramAdmin(ModelAdmin):
    list_display = ('id', 'nome', 'funcao', 'status')
    search_fields = ['nome',]
    list_display_links = list_display


@register(ApiTelegram)
class ApiTelegramAdmin(ModelAdmin):
    list_display = ('id', 'hash')


@register(BotTelegram)
class BotTelegramAdmin(ModelAdmin):
    list_display = ('id', 'nome', 'token')
    search_fields = ['nome',]
