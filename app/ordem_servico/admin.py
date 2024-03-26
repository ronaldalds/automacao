from django.contrib.admin import ModelAdmin, register
from django.contrib import messages
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from reversion.admin import VersionAdmin
from import_export import resources
from import_export.admin import ImportExportMixin
from .processo import Ordem
from .models import OrdemServico
from .models import ThreadOs


@register(ThreadOs)
class ThreadAdmin(ModelAdmin):
    list_display = (
        'id',
        'numero_thread',
    )
    list_display_links = list_display


class OsResource(resources.ModelResource):
    class Meta:
        model = OrdemServico

    def before_import_row(self, row, **kwargs):
        mandatory_fields = (
            'mk',
            'conexao_associada',
            'documento',
            'grupo_atendimento_os',
            'status',
        )
        missing_fields = [
            field for field in mandatory_fields if row.get(field) is None
        ]
        if missing_fields:
            messages = [f"Error no campo: {msg}" for msg in missing_fields]
            raise ValidationError(messages)


def processo_os(item: OrdemServico):
    if not item.processamento:
        return None
    item.processamento = False
    ordem_servico = Ordem(item)
    ordem_servico.os()


@register(OrdemServico)
class OrdemServicoAdmin(ImportExportMixin, VersionAdmin):
    def os(modeladmin, request, queryset):
        limite_threads = ThreadOs.objects.get(pk=1).numero_thread
        queryset = queryset.filter(
            status=False,
            processamento=False
        )
        for query in queryset:
            query.processamento = True
            query.save()

        def execute_cancelar(queryset):
            with ThreadPoolExecutor(max_workers=limite_threads) as executor:
                executor.map(processo_os, queryset)

        # Criando e iniciando o thread
        thread = Thread(target=execute_cancelar, args=(queryset,))
        thread.start()
        messages.success(
            request,
            f'Foi iniciado {len(queryset)} cancelamentos'
        )

    os.short_description = "O.S"

    actions = [os]
    resource_class = OsResource
    list_display = (
        'id',
        'mk',
        'cod_pessoa',
        'qtd_conexoes',
        'conexao_associada',
        'os_cancelamento_ou_recolhimento',
        'documento',
        'tipo_os',
        'grupo_atendimento_os',
        'detalhes_os',
        'nivel_sla',
        'status',
        'processamento',
        'observacao',
        'created_at',
    )
    list_filter = ('mk', 'status', 'grupo_atendimento_os')
    search_fields = ['contrato', 'conexao_associada']
    readonly_fields = ('created_at',)
