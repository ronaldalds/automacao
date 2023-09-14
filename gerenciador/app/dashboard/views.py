from django.shortcuts import render
from .util import Desk

# Create your views here.
FLAG = 1
def ajuste_chamados(chamados: [dict]):

    assunto = dict.get("Assunto")
    operador = dict.get("NomeOperador", "Na Fila")
    cod_chamado = dict.get("CodChamado")
    data_criacao = dict.get("DataCriacao")
    return 

def dashboard(request, *args, **kwargs):
    global FLAG
    desk = Desk()

    if FLAG == 1:
        response: dict = desk.relatorio("100").get("root")
        titulo = 'Sistemas'
        chamados = response
        qtd_chamados = len(chamados)
        status = 'bg-success' if qtd_chamados == 0 else 'bg-danger'
        FLAG = 0
    else:
        response = desk.relatorio("102").get("root").get("root")
        titulo = 'Suporte a T.I.'
        chamados = response
        qtd_chamados = len(chamados)
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