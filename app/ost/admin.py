from django.contrib import admin
from .models import (
    TipoOs,
    TecnicoMensagem,
    TempoSla,
    InformacaoOs,
    Log,
    ErrorOs,
)


@admin.register(TipoOs)
class TipoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'sla', 'status')
    search_fields = ['tipo',]


@admin.register(TecnicoMensagem)
class TecnicoMensagemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome_tecnico',
        'chat_id',
        'sla',
        'cod_os',
        'data_envio',
        'status'
    )
    list_filter = ('chat_id',)
    search_fields = ['chat_id',]


@admin.register(TempoSla)
class TempoSLAAdmin(admin.ModelAdmin):
    list_display = ('sla',)
    search_fields = ['sla',]


@admin.register(InformacaoOs)
class InformacaoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_tipo_os', 'nome')
    list_filter = ('id_tipo_os',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_envio')
    list_filter = ('data_envio',)


@admin.register(ErrorOs)
class ErrorOsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'os',
        'tipo',
        'operador',
        'detalhe',
        'created_at',
    )
    list_filter = ('operador',)
