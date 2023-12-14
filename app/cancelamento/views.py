from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CancelamentoSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Cancelamento


# Create your views here.
class CancelamentoViewSet(ModelViewSet):
    queryset = Cancelamento.objects.filter(status=False)
    serializer_class = CancelamentoSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
