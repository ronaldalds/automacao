from abc import ABC, abstractmethod


class Coin(ABC):
    def __init__(
        self,
        title: str,
        id: str,
    ) -> None:
        self._title: str = title
        self._id: str = id

    @abstractmethod
    def title(self) -> str:
        pass

    @abstractmethod
    def id(self) -> str:
        pass

    def xpath(self) -> str:
        return f'//*[@id="{self._id}"]'


class Crm(Coin):
    def __init__(self) -> None:
        super().__init__(title="CRM", id="1791381")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Gestao(Coin):
    def __init__(self) -> None:
        super().__init__(title="Gestão", id="1856707")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Financeiro(Coin):
    def __init__(self) -> None:
        super().__init__(title="Financeiro", id="946094")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Workspace(Coin):
    def __init__(self) -> None:
        super().__init__(title="Workspace", id="1833270")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Estoque(Coin):
    def __init__(self) -> None:
        super().__init__(title="Estoque", id="1200344")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Tecnico(Coin):
    def __init__(self) -> None:
        super().__init__(title="Técnico", id="1511788")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Integradores(Coin):
    def __init__(self) -> None:
        super().__init__(title="Integradores", id="169073")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id



class Maps(Coin):
    def __init__(self) -> None:
        super().__init__(title="Maps", id="1162115")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id


class Suporte(Coin):
    def __init__(self) -> None:
        super().__init__(title="Suporte", id="1631783")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id


class Ajuda(Coin):
    def __init__(self) -> None:
        super().__init__(title="Ajuda", id="1185636")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id


class Home(Coin):
    def __init__(self) -> None:
        super().__init__(title="Home", id="1504596")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id


class Configuracoes(Coin):
    def __init__(self) -> None:
        super().__init__(title="Configurações", id="545976")
    
    def title(self) -> str:
        return self._title

    def id(self) -> str:
        return self._id