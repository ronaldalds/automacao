from django.contrib.admin import ModelAdmin, register
from .models import (
    TipoOs,
    TecnicoMensagem,
    TempoSla,
    InformacaoOs,
    Log,
    ErrorOs,
)


@register(TipoOs)
class TipoOSAdmin(ModelAdmin):
    list_display = ('id', 'tipo', 'sla', 'status')
    search_fields = ['tipo',]


@register(TecnicoMensagem)
class TecnicoMensagemAdmin(ModelAdmin):
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


@register(TempoSla)
class TempoSLAAdmin(ModelAdmin):
    list_display = ('sla',)
    search_fields = ['sla',]


@register(InformacaoOs)
class InformacaoOSAdmin(ModelAdmin):
    list_display = ('id', 'id_tipo_os', 'nome')
    list_filter = ('id_tipo_os',)


@register(Log)
class LogAdmin(ModelAdmin):
    list_display = ('id', 'data_envio')
    list_filter = ('data_envio',)


@register(ErrorOs)
class ErrorOsAdmin(ModelAdmin):
    list_display = (
        'id',
        'os',
        'tipo',
        'operador',
        'detalhe',
        'created_at',
    )
    list_filter = ('operador',)
