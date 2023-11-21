from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin

# Register your models here.
@admin.register(Cancelamento)
class CancelamentoAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'mk',
        'contrato',
        'cod_pessoa',
        'conexao',
        'os_cancelamento_30d',
        'documento_codigo',
        'tipo_os',
        'planos_de_contas',
        'relato_do_problema',
        'detalhes_cancelamento',
        'grupo_atendimento_os',
        'incidencia_de_multa',
        'valor_multa',
        'data_vcto_multa_contratual',
        'data_a_cancelar',
        'loja',
        'onu_serial',
        'status',
        'last_edited_by',
    )
    list_display_links = list_display
    list_filter = ('status', 'mk',)
    search_fields = ['contrato','cod_pessoa', 'conexao', 'documento_codigo']
    
    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)