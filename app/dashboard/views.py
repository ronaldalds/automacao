from django.shortcuts import render, redirect
from .util import Desk
import os

# Create your views here.
FLAG = 1

def dashboard(request, *args, **kwargs):
    global FLAG
    desk = Desk()

    if FLAG == 1:
        response: dict = desk.relatorio(os.environ.get("ID_RELATORIO_DESK_SISTEMAS"))
        titulo = 'Sistemas'
        qtd_chamados = response.get("total", 0)
        chamados = response.get("root").get("root") if qtd_chamados == 0 else response.get("root")
        status = 'bg-success' if qtd_chamados == 0 else 'bg-danger'
        FLAG = 0

    else:
        response: dict = desk.relatorio(os.environ.get("ID_RELATORIO_DESK_SUPORTE_TI"))
        titulo = 'Suporte a T.I.'
        qtd_chamados = response.get("total", 0)
        chamados = response.get("root").get("root") if qtd_chamados == 0 else response.get("root")
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