from rest_framework import serializers
from .models import *

# Serializers define the API representation.


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ["id", "nome", "login_mk", "chat_id", "status",]


class TipoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOS
        fields = ["id", "tipo", "sla",]


class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = ["id", "tecnico_id", "alerta_id", "mensagem", "cod_os", "data_envio", "status",]


class AlertaSLASerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaSLA
        fields = ["id", "hora",]


class InformacaoOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoOS
        fields = ["id", "id_tipo_os", "nome",]