from rest_framework import serializers
from .models import *

# Serializers define the API representation.


class CancelamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancelamento
        fields = [
            "id",
            "mk",
            "contrato",
            "atraso",
            "cod_pessoa",
            "conexao",
            "documento",
            "tipo_os",
            "planos_de_contas",
            "relato_do_problema",
            "detalhes_cancelamento",
            "grupo_atendimento_os",
            "incidencia_de_multa",
            "valor_multa",
            "data_vcto_multa_contratual",
            "data_a_cancelar",
            "loja",
            "onu_serial",
            "status_cancelamento",
        ]