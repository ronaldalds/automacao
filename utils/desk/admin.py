from django.contrib.admin import ModelAdmin, register
from .models import (
    TokenDesk,
    StatusDesk,
    FormaAtendimentoDesk,
)


@register(TokenDesk)
class TokenDeskAdmin(ModelAdmin):
    list_display = (
        'id',
        'nome',
        'operador',
        'ambiente',
    )
    list_display_links = list_display


@register(StatusDesk)
class StatusDeskAdmin(ModelAdmin):
    list_display = (
        'nome',
        'id',
    )
    list_display_links = list_display


@register(FormaAtendimentoDesk)
class FormaAtendimentoDeskAdmin(ModelAdmin):
    list_display = (
        'nome',
        'id',
    )
    list_display_links = list_display
