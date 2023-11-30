from .models import *
from django.contrib import admin
from import_export import resources
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from django.core.exceptions import ValidationError

class CancelamentoResource(resources.ModelResource):
    class Meta:
        model = Cancelamento

    def before_import_row(self, row, **kwargs):
        mandatory_fields = (
            'mk',
            'contrato',
            'cod_pessoa',
            'documento_codigo',
            'tipo_os',
            'planos_de_contas',
            'relato_do_problema',
            'detalhes_cancelamento',
            'grupo_atendimento_os',
            'incidencia_de_multa',
            'valor_multa',
            'data_vcto_multa_contratual',
        )
        missing_fields = [
            field for field in mandatory_fields if row.get(field) is None
        ]
        if missing_fields:
            messages = [f"Error no campo: {msg}" for msg in missing_fields]
            raise ValidationError(messages)

        
@admin.register(Cancelamento)
class CancelamentoAdmin(ImportExportMixin, VersionAdmin):
    resource_class = CancelamentoResource
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
        'observacao',
    )
    list_display_links = list_display
    list_filter = ('status', 'mk',)
    search_fields = ['contrato','cod_pessoa', 'conexao', 'documento_codigo']