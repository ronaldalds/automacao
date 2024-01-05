from django.contrib import admin
from .models import OsGoon, StatusInfo


@admin.register(OsGoon)
class OsGoonAdmin(admin.ModelAdmin):
    list_display = (
        'numero_os',
        'ordem_servico_externa',
        'descricao',
        'tipo_servico'
    )
    list_filter = ('tipo_servico',)
    search_fields = ['ordem_servico_externa',]


@admin.register(StatusInfo)
class StatusInfoAdmin(admin.ModelAdmin):
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
