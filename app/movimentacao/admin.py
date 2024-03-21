from django.contrib.admin import ModelAdmin, register
from django.contrib import messages
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from reversion.admin import VersionAdmin
from import_export import resources
from import_export.admin import ImportExportMixin
from .processo import Movimentar
from .models import Movimentacao, ThreadMovimentacao


@register(ThreadMovimentacao)
class ThreadMovimentacaoAdmin(ModelAdmin):
    list_display = (
        'id',
        'numero_thread',
    )
    list_display_links = list_display


class MovimentacaoResource(resources.ModelResource):
    class Meta:
        model = Movimentacao

    def before_import_row(self, row, **kwargs):
        mandatory_fields = (
            'id',
        )
        missing_fields = [
            field for field in mandatory_fields if row.get(field) is None
        ]
        if missing_fields:
            message = [f"Error no campo: {msg}" for msg in missing_fields]
            raise ValidationError(message)


def processo_movimentacao(item: Movimentacao):
    if not item.processamento:
        return None
    item.processamento = False
    movimentacao = Movimentar(item)
    movimentacao.movimentar()


def execute_cancelar(queryset):
    limite_threads = ThreadMovimentacao.objects.get(pk=1).numero_thread
    with ThreadPoolExecutor(max_workers=limite_threads) as executor:
        executor.map(processo_movimentacao, queryset)


@register(Movimentacao)
class MovimentacaoAdmin(ImportExportMixin, VersionAdmin):
    def movimentar(modeladmin, request, queryset: list[Movimentacao]):
        queryset = queryset.filter(status=False, processamento=False)
        for query in queryset:
            query.processamento = True
            query.save()

        # Criando e iniciando o thread
        thread = Thread(target=execute_cancelar, args=(queryset,))
        thread.start()
        messages.success(
            request,
            f'Foi iniciado {len(queryset)} movimentações'
        )

    def tirar_processamento(modeladmin, request, queryset: list[Movimentacao]):
        queryset = queryset.filter(status=False, processamento=True)
        for query in queryset:
            query.processamento = False
            query.save()

    movimentar.short_description = "Movimentar"
    tirar_processamento.short_description = "Tirar Processamento"

    actions = [movimentar, tirar_processamento]
    resource_class = MovimentacaoResource
    list_display = (
        'id',
        'status',
        'processamento',
        'created_at',
        'observacao',
    )
    list_display_links = list_display
    list_filter = ("status", "processamento", "created_at")
    search_fields = ['id']
