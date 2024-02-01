from rest_framework import serializers
from .models import Alerta


class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = [
            "id",
            "automovel",
            "placa",
            "velocidade",
            "horario",
            "enviado",
        ]
