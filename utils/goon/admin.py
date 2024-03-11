from django.contrib.admin import ModelAdmin, register
from .models import TokenGoon, StatusGoon


@register(TokenGoon)
class TokenGoonAdmin(ModelAdmin):
    list_display = (
        'id',
        'nome',
        'auth',
        'cliente',
    )
    list_display_links = list_display


@register(StatusGoon)
class StatusGoonAdmin(ModelAdmin):
    list_display = (
        'nome',
        'descricao',
    )
    list_display_links = list_display
