from django.contrib.admin import ModelAdmin, register
from .models import Chamado, Interacao


@register(Chamado)
class ChamadoAdmin(ModelAdmin):
    list_display = (
        "id",
        "nome_categoria",
        "data_finalizacao",
        "nome_operador",
        "nome_sla_status_atual",
        "nome_sistema",
        )

    list_filter = (
        "nome_categoria",
        "nome_operador",
    )

    search_fields = [
        "id",
        "nome_categoria",
    ]

    readonly_fields = [
        "total_horas_1_atendimento",
        "total_horas_1_2_atendimento",
        "tempo_restante_1",
        "tempo_restante_2",
    ]


@register(Interacao)
class InteracaoAdmin(ModelAdmin):
    list_display = (
        "chamado",
        "seguencia",
        "status_acao_nome_relatorio",
        "fantasia_fornecedor",
        "chamado_aprovadores",
        "tempo_corrido_interacao",
    )

    search_fields = [
        "chamado__id",
        "chamado__assunto",
    ]

    readonly_fields = [
        "tempo_corrido_interacao",
    ]
