from rest_framework import serializers
from .models import (
    Tecnico,
    TipoOs,
    TecnicoMensagem,
    TempoSla,
    SlaOs,
    InformacaoOs,
    Log
)

# Serializers define the API representation.


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'


class TipoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOs
        fields = '__all__'


class TecnicoMensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TecnicoMensagem
        fields = '__all__'


class TempoSLASerializer(serializers.ModelSerializer):
    class Meta:
        model = TempoSla
        fields = '__all__'


class SlaOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlaOs
        fields = '__all__'


class InformacaoOSSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InformacaoOs
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
