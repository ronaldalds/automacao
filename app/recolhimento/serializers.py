from rest_framework import serializers
from .models import *

# Serializers define the API representation.


class RecolhimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recolhimento
        fields = ['id',
                  'mk',
                  'contrato',
                  'qtd_conexoes',
                  'conexao_associada',
                  'qtd_atendimentos',
                  'os_cancelamento_ou_recolhimento',
                  'documento',
                  'tipo_os',
                  'planos_de_contas',
                  'grupo_atendimento_os',
                  'detalhes_os',
                  'atraso_max',
                  'loja',
                  'status_recolhimento',
                  ]