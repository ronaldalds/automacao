from django.contrib.admin import ModelAdmin, register
from .models import OsGoon, StatusInfo


@register(OsGoon)
class OsGoonAdmin(ModelAdmin):
    list_display = (
        'numero_os',
        'ordem_servico_externa',
        'descricao',
        'tipo_servico'
    )
    list_filter = ('tipo_servico',)
    search_fields = ['ordem_servico_externa',]


@register(StatusInfo)
class StatusInfoAdmin(ModelAdmin):
    list_display = (
        'id',
        'sequencia',
        'status',
        'data',
        'mobile_agent',
        'mobile_phone',
        'os_goon',
        'enviado',
    )
    list_filter = ('enviado',)
    search_fields = ['os_goon',]
