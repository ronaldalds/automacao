from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from reversion.admin import VersionAdmin
from import_export import resources
from import_export.admin import ImportExportMixin
from .processo import Cancelar
from .models import Cancelamento
from .models import ThreadCancelamento


@admin.register(ThreadCancelamento)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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
            'tipo_os',
            'defeito',
            'profile',
            'planos_de_contas',
            'relato_do_problema',
            'detalhes_cancelamento',
            'grupo_atendimento_os',
            'incidencia_de_multa',
            'data_vcto_multa_contratual',
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
        queryset = queryset.filter(status=False, processamento=False)
        for query in queryset:
            query.processamento = True
            query.save()

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
        'tipo_os',
        'defeito',
        'profile',
        'planos_de_contas',
        'relato_do_problema',
        'detalhes_cancelamento',
        'grupo_atendimento_os',
        'incidencia_de_multa',
        'data_vcto_multa_contratual',
        'motivo_cancelamento',
        'valor_multa',
        'status',
        'processamento',
        'observacao',
        'created_at',
    )
    list_display_links = list_display
    list_filter = ('mk', 'status', 'processamento', 'created_at')
    search_fields = ['contrato', 'cod_pessoa',]
    readonly_fields = ('created_at',)
