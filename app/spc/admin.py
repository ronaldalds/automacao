from django.contrib.admin import ModelAdmin, register
from .models import Spc


@register(Spc)
class SpcAdmin(ModelAdmin):
    list_display = (
        'id',
        'nome_consumidor',
        'documento',
        'cod_cliente',
        'valor_do_debito',
        'status_spc',
    )
    list_display_links = list_display
    list_filter = ('status_spc', 'cep',)
    search_fields = [
        'nome_consumidor',
        'documento',
        'cod_cliente',
    ]
