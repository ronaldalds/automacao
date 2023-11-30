from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *


class TecnicoViewSet(ModelViewSet):
    queryset = Tecnico.objects.filter(status=True)
    serializer_class = TecnicoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")


class TipoOSViewSet(ModelViewSet):
    queryset = TipoOS.objects.all()
    serializer_class = TipoOSSerializer


class TecnicoMensagemViewSet(ModelViewSet):
    queryset = TecnicoMensagem.objects.all()
    serializer_class = TecnicoMensagemSerializer


class TempoSLAViewSet(ModelViewSet):
    queryset = TempoSLA.objects.all()
    serializer_class = TempoSLASerializer


class SlaOSViewSet(ModelViewSet):
    queryset = SlaOS.objects.all()
    serializer_class = SlaOSSerializer


class InformacaoOSViewSet(ModelViewSet):
    queryset = InformacaoOS.objects.all()
    serializer_class = InformacaoOSSerializer


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer