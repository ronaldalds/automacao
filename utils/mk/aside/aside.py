from abc import ABC


class Aside(ABC):
    def __init__(
        self,
        painel: str,
        id: str,
    ) -> None:
        self._painel: str = painel
        self._id: str = id

    def painel(self) -> str:
        return self._painel

    def id(self) -> str:
        return self._id

    def xpath(self) -> str:
        return f'//*[@id="{self._id}"]'
