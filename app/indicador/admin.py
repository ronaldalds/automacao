from django.contrib import admin
from .models import Chamado, Interacao


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "assunto",
        "data_criacao",
        "data_finalizacao",
        "nome_categoria",
        "nome_operador",
        "first_call",
        "sla_2_expirado",
        "nome_sla_status_atual",

        # Total horas primeiro segundo atendimento
        "total_horas_1_2_atendimento_str",
        "total_horas_1_2_atendimento",
        # ----------------------------------------------------------------
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
        "total_horas_1_2_atendimento",
    ]


@admin.register(Interacao)
class InteracaoAdmin(admin.ModelAdmin):
    list_display = (
        "chamado",
        "status_acao_nome_relatorio",
        "fantasia_fornecedor",
        "seguencia",
    )

    search_fields = [
        "chamado__id",
        "chamado__assunto",
    ]
