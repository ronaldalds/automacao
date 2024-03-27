from utils.mk.drive import Mk
from datetime import datetime, timedelta
from utils.mk.models import Login
from utils.mk.models import Faturamento as RegraFaturamento
from utils.mk.coin.coin import Financeiro
from utils.mk.aside.aside_financeiro import Faturamento
from .models import FaturamentoLog
import random


class FaturamentoProcesso:
    def __init__(self, mk: int):
        self.mk = mk
        self.faturamento = Faturamento()
        self.financeiro = Financeiro()
        self.browser: Mk
        self.login_mk: Login

    def message_error(self, message: str) -> None:
        FaturamentoLog.objects.create(mk=self.mk, status=False, observacao=message)
        self.browser.close()

    def message_sucess(self, message: str) -> None:
        FaturamentoLog.objects.create(mk=self.mk, status=True, observacao=message)
        self.browser.close()

    def regra(self):
        dia = datetime.now()
        dia_faturamento = dia + timedelta(days=9)
        regra = RegraFaturamento.objects.filter(mk=self.mk, dia_faturamento=dia_faturamento.day).first()
        if regra:
            filtro = FaturamentoLog.objects.filter(
                mk=self.mk,
                data_faturamento=dia.date(),
                status=True
            ).exists()
            if not filtro:
                self.faturar(dia=dia, regra=regra)

    def faturar(self, dia: datetime, regra: RegraFaturamento) -> None:
        print(f"Iniciou Faturamento: {datetime.now().date()}")
        # return self.message_sucess("foi")
        try:
            self.login_mk = Login.objects.get(mk=self.mk)
            self.browser = Mk(
                username=self.login_mk.username,
                password=self.login_mk.password,
                url=self.login_mk.url,
            )
            self.browser.login()

        except Exception as e:
            return self.message_error(f"Error instância: {e}")

        # fechar tela de complete seu cadastro
        try:
            self.browser.iframeMain()
            self.browser.click('//div[@class="OptionClose"]')
        except Exception as e:
            print(f"Warning tela cadastro: {e}")

        # clique moeda financeiro
        try:
            self.browser.iframeCoin()
            self.browser.click(self.financeiro.xpath())
        except Exception as e:
            return self.message_error(f"Error clique moeda financeiro: {e}")

        return self.message_sucess("Success!")
