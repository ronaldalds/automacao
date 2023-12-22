from desk.desk_drive import Desk
from django.shortcuts import render


# Create your views here.
FLAG = 1
desk = Desk()


def dashboard(request, *args, **kwargs):
    global FLAG

    if FLAG == 1:
        response: dict = desk.relatorio("100")
        titulo = 'Sistemas'
        qtd_chamados = response.get("total", 0)
        if qtd_chamados == 0:
            chamados = response.get("root").get("root")
        else:
            chamados = response.get("root")
        status = 'bg-success' if qtd_chamados == 0 else 'bg-danger'
        FLAG = 0

    else:
        response: dict = desk.relatorio("102")
        titulo = 'Suporte a T.I.'
        qtd_chamados = response.get("total", 0)
        if qtd_chamados == 0:
            chamados = response.get("root").get("root")
        else:
            chamados = response.get("root")
        status = 'bg-success' if qtd_chamados == 0 else 'bg-danger'
        FLAG = 1

    context = {
        "titulo": titulo,
        "qtd_chamados": qtd_chamados,
        "status": status,
        "chamados": chamados,
    }

    return render(
        request,
        "dashboard/index.html",
        context=context
    )
