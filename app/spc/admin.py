from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Spc)
class SpcAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'nome_consumidor',
                    'documento',
                    'cod_cliente',
                    'valor_do_debito',
                    'status_spc',
                    )
    list_filter = ('status_spc', 'cep',)
    search_fields = ['nome_consumidor','documento', 'cod_cliente',]