from rest_framework import serializers
from .models import Cancelamento

# Serializers define the API representation.


class CancelamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancelamento
        fields = [
            'id',
            'mk',
            'grupo_atendimento_os',
            'status',
            'observacao',
        ]
