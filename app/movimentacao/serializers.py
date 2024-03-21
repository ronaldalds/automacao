from rest_framework import serializers
from .models import Movimentacao

# Serializers define the API representation.


class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'mk',
            'status',
            'processamento',
            'observacao',
        ]
