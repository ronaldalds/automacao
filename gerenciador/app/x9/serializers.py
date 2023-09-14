from rest_framework import serializers
from .models import *

# Serializers define the API representation.

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