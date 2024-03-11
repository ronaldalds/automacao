from django.contrib.admin import ModelAdmin, register
from .models import Chamado, Interacao


@register(Chamado)
class ChamadoAdmin(ModelAdmin):
    list_display = (
        "id",
        "nome_categoria",
        "nome_operador",
        "data_finalizacao",
        "sla_1_expirado",
        "total_horas_1_atendimento_str",
        "sla_2_expirado",
        "total_horas_1_2_atendimento_str",
        "nome_status",
        )

    list_filter = (
        "nome_categoria",
        "nome_operador",
        "nome_status",
    )

    search_fields = [
        "id",
        "assunto",
    ]

    readonly_fields = [
        "total_horas_1_atendimento",
        "total_horas_1_2_atendimento",
    ]


@register(Interacao)
class InteracaoAdmin(ModelAdmin):
    list_display = (
        "chamado",
        "status_acao_nome_relatorio",
        "fantasia_fornecedor",
        "chamado_aprovadores",
        "seguencia",
        "tempo_corrido_interacao_str",
    )

    search_fields = [
        "chamado__id",
        "chamado__assunto",
    ]

    readonly_fields = [
        "tempo_corrido_interacao",
    ]
