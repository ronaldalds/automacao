from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    TecnicoSerializer,
    TipoOSSerializer,
    TecnicoMensagemSerializer,
    TempoSLASerializer,
    SlaOSSerializer,
    InformacaoOSSerializer,
    LogSerializer
)
from .models import (
    Tecnico,
    TipoOs,
    TecnicoMensagem,
    TempoSla,
    SlaOs,
    InformacaoOs,
    Log
)


class TecnicoViewSet(ModelViewSet):
    queryset = Tecnico.objects.filter(status=True)
    serializer_class = TecnicoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")


class TipoOSViewSet(ModelViewSet):
    queryset = TipoOs.objects.all()
    serializer_class = TipoOSSerializer


class TecnicoMensagemViewSet(ModelViewSet):
    queryset = TecnicoMensagem.objects.all()
    serializer_class = TecnicoMensagemSerializer


class TempoSLAViewSet(ModelViewSet):
    queryset = TempoSla.objects.all()
    serializer_class = TempoSLASerializer


class SlaOSViewSet(ModelViewSet):
    queryset = SlaOs.objects.all()
    serializer_class = SlaOSSerializer


class InformacaoOSViewSet(ModelViewSet):
    queryset = InformacaoOs.objects.all()
    serializer_class = InformacaoOSSerializer


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
