from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import MovimentacaoSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Movimentacao


# Create your views here.
class MovimentacaoViewSet(ModelViewSet):
    queryset = Movimentacao.objects.filter(status=False)
    serializer_class = MovimentacaoSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
