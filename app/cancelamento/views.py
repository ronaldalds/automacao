from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from .models import Cancelamento
from rest_framework.response import Response

# Create your views here.
class CancelamentoViewSet(ViewSet):
    def cancelar(self, request):
        query = Cancelamento.objects.filter(status=False)
        