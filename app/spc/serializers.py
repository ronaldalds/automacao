from rest_framework import serializers
from .models import *

# Serializers define the API representation.


class SpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spc
        fields = ['id',
                  'cod_cliente',
                  'data_vencimento',
                  'data_compra',
                  'valor_do_debito',
                  'faturas_vencidas',
                  'tipo_de_pessoa',
                  'documento',
                  'nome_consumidor',
                  'cep',
                  'logradouro',
                  'numero',
                  'complemento',
                  'bairro',
                  'ddd',
                  'celular',
                  'email',
                  'data_nascimento',
                  'status_spc',
                  ]