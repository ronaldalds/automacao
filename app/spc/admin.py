from django.contrib import admin
from .models import Spc


@admin.register(Spc)
class SpcAdmin(admin.ModelAdmin):
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
