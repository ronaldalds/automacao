from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Cancelamento)
class CancelamentoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'mk',
                    'contrato',
                    'cod_pessoa',
                    'documento',
                    'status_cancelamento',
                    )
    list_filter = ('status_cancelamento', 'mk',)
    search_fields = ['contrato','cod_pessoa', 'grupo_atendimento_os',]