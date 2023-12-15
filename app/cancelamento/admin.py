from threading import Thread
from .processo import Cancelar
from django.contrib import admin
from .models import Cancelamento
from import_export import resources
from django.contrib import messages
from .models import ThreadCancelamento
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor


@admin.register(ThreadCancelamento)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'numero_thread',
    )
    list_display_links = list_display


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
            'defeito',
            'profile',
            'planos_de_contas',
            'relato_do_problema',
            'detalhes_cancelamento',
            'grupo_atendimento_os',
            'incidencia_de_multa',
            'data_vcto_multa_contratual',
            'data_a_cancelar',
            'motivo_cancelamento',
            'valor_multa',
        )
        missing_fields = [
            field for field in mandatory_fields if row.get(field) is None
        ]
        if missing_fields:
            messages = [f"Error no campo: {msg}" for msg in missing_fields]
            raise ValidationError(messages)


def processo_cancelamento(item: Cancelamento):
    cancelamento = Cancelar(item)
    cancelamento.cancelar()


@admin.register(Cancelamento)
class CancelamentoAdmin(ImportExportMixin, VersionAdmin):
    def cancelar(modeladmin, request, queryset: list[Cancelamento]):
        limite_threads = ThreadCancelamento.objects.get(pk=1).numero_thread
        print(limite_threads)

        def execute_cancelar(queryset):
            with ThreadPoolExecutor(max_workers=limite_threads) as executor:
                executor.map(processo_cancelamento, queryset)

        # Criando e iniciando o thread
        thread = Thread(target=execute_cancelar, args=(queryset,))
        thread.start()
        messages.success(
            request,
            f'Foi iniciado {len(queryset)} cancelamentos'
        )

    cancelar.short_description = "Cancelar conexão"

    actions = [cancelar]
    resource_class = CancelamentoResource
    list_display = (
        'id',
        'mk',
        'contrato',
        'cod_pessoa',
        'conexao',
        'documento_codigo',
        'tipo_os',
        'defeito',
        'profile',
        'planos_de_contas',
        'relato_do_problema',
        'detalhes_cancelamento',
        'grupo_atendimento_os',
        'incidencia_de_multa',
        'data_vcto_multa_contratual',
        'data_a_cancelar',
        'loja',
        'onu_serial',
        'status',
        'motivo_cancelamento',
        'os_cancelamento_30d',
        'valor_multa',
        'observacao',
    )
    list_display_links = list_display
    list_filter = ('status', 'mk',)
    search_fields = ['contrato', 'cod_pessoa', 'conexao', 'documento_codigo']
