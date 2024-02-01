from django.contrib import admin
from .models import (
    UserTelegram,
    ApiTelegram,
    BotTelegram,
)


@admin.register(UserTelegram)
class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'funcao', 'status')
    search_fields = ['nome',]
    list_display_links = list_display


@admin.register(ApiTelegram)
class ApiTelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash')


@admin.register(BotTelegram)
class BotTelegramAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'token')
    search_fields = ['nome',]
