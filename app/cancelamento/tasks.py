from celery import shared_task
# from .models import Cancelamento
# from .processo import Cancelar


@shared_task
def processo_cancelamento(item):
    # query = Cancelamento.objects.get(id=item)
    return item
    # cancelamento = Cancelar(query)
    # cancelamento.cancelar()