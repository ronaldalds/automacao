from .aside import Aside


class CrmHome(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='CRM - Home', id='454751')


class PainelDinamico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='RD - CRM', id='388243')


class GerenciadorDeInviabilidades(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Inviabilidades', id='1052995')


class GerenciadorDeFechamento(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Fechamento', id='539320')


class GerenciadorDePosVenda(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Pós-Venda', id='213393')


class GerenciadorDeMetas(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Metas', id='267807')


class GerenciadorDeComissoes(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Comissões', id='887989')


class GerenciadorDeCancelamento(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Cancelamento', id='1406061')


class MapaDeCrm(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Mapa de CRM', id='1998852')
