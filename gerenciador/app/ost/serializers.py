from rest_framework import serializers
from .models import *

# Serializers define the API representation.


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'


class TipoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOS
        fields = '__all__'


class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = '__all__'


class AlertaSLASerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaSLA
        fields = '__all__'


class InformacaoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoOS
        fields = '__all__'