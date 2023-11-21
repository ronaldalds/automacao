from .aside import Aside


class WorkspaceHome(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Workspace - Home', id='166385')


class PainelDinamico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='RD - Workspace', id='555968')


class MkbotAssistant(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='MKBot Assistant', id='1843438')


class MkbotChat(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='', id='824589')


class AgendamentoDiagnostico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Workspace - Diagnósticos - Agenda', id='759593')


class AtendimentoDiagnostico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Workspace - Diagnósticos - Atendimento', id='1414703')



class AtendimentoPainel(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel Atendimento', id='681671')


class OsAgenda(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Agenda das O.S.', id='58874')


class OsDiagnostico(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Workspace - Diagnósticos - OS', id='1239736')


class OsMapa(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='', id='1811217')


class OsPainel(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel O.S.', id='1117358')


class PessoasOuEmpresas(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Workspace - painel - pessoas', id='176177')


class PainelDeRecados(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel de Recados', id='263933')


class PainelDeTarefas(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Painel de Tarefas', id='871824')


class ChatPainel(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='Chat - Painel', id='25100')


class SmsPainel(Aside):
    def __init__(self,) -> None:
        super().__init__(painel='SMS - Painel', id='418523')
