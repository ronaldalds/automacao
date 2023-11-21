from .aside import Aside


class EstoqueHome(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Estoque - Home', id='465955')


class PainelDinamico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='RD - Estoque', id='1947945')


class Compra(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Estoque - Painel - Compra', id='508868')


class Estoquista(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel do Estoquista',id='1638245')


class GerenciadorDeIds(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de IDs',id='1377474')


class GerenciadorDeImobilizados(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de Imobilizados',id='589689')


class GerenciadorDeVeiculos(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Gerenciador de veículos',id='583121')


class PainelDeDevolucao(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel de Devolução',id='1314265')


class PainelDeNotas(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel de Notas (NF-e / NFS-e)', id='1729850')


class Rastreabilidade(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel de Rastreabilidade de Estoque', id='1627534')


class MovimentacaoSaidas(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Estoque - Painel - Venda / Comodato', id='279678')
