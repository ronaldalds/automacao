from time import sleep
from .models import Cancelamento
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import CancelamentoSerializer
from concurrent.futures import ThreadPoolExecutor
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from scraping.cancelamento.processo_cancelamento import ProcessoCancelamento

running = False


# Create your views here.
class CancelamentoViewSet(ViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def _processo(self, conexao: Cancelamento):
        if running:
            cancelamento = ProcessoCancelamento(conexao)
            return cancelamento.cancelar()
        else:
            return None

    @swagger_auto_schema(responses={200: CancelamentoSerializer(many=True)})
    def cancelar(self, request):
        global running
        # Verifica se tem algum processo em execução
        if running:
            return Response(
                {"status": "Cancelamento em execução"},
                status=409
            )

        # Muda a variável para em execução
        running = True

        # Limita o tamanho da pool
        threads = 5

        # Pesquisa na base o que tem de cancelamento para ser executado
        conexoes: list[Cancelamento] = list(
            Cancelamento.objects.filter(status=False)
        )

        # Executa a pool
        with ThreadPoolExecutor(max_workers=threads) as executor:
            resultados = executor.map(self._processo, conexoes)

        # Salva os resultados do processo no banco
        for resultado in resultados:
            if resultado:
                resultado.save()

        # serializa a pesquisa e responde a solicitação
        serializer = CancelamentoSerializer(conexoes, many=True)
        running = False
        return Response(serializer.data)

    def parar_cancelamento(self, request):
        global running
        if running:
            running = False
            return Response(
                {"status": "Pedido de parada do cancelamento iniciado..."},
                status=200
            )
        else:
            return Response(
                {"status": "Cancelamento parado"},
                status=200
            )
