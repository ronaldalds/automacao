from django.contrib import admin
from .models import (
    TokenDesk,
    StatusDesk,
    FormaAtendimentoDesk,
)


@admin.register(TokenDesk)
class TokenDeskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'operador',
        'ambiente',
    )
    list_display_links = list_display


@admin.register(StatusDesk)
class StatusDeskAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'id',
    )
    list_display_links = list_display


@admin.register(FormaAtendimentoDesk)
class FormaAtendimentoDeskAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'id',
    )
    list_display_links = list_display
