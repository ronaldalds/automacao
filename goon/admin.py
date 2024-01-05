from django.contrib import admin
from .models import TokenGoon, StatusGoon


@admin.register(TokenGoon)
class TokenGoonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'auth',
        'cliente',
    )
    list_display_links = list_display


@admin.register(StatusGoon)
class StatusGoonAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'id',
    )
    list_display_links = list_display