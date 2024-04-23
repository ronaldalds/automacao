from utils.mk.drive import Mk
from datetime import datetime, timedelta
from utils.mk.models import Login
from selenium.webdriver.common.keys import Keys
from utils.mk.models import Faturamento as RegraFaturamento
from utils.mk.coin.coin import Financeiro
from utils.mk.aside.aside_financeiro import Faturamento
from .models import FaturamentoLog
from time import sleep


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
        dia_faturamento = dia + timedelta(days=8)
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
        print(f"Iniciou Faturamento: {dia.date()}")
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

        # clique aside Faturamento
        try:
            self.browser.iframeAsideCoin(self.financeiro)
            self.browser.click(self.faturamento.xpath())
        except Exception as e:
            return self.message_error(f"Error clique aside faturamento: {e}")

        # clique novo faturamento
        try:
            self.browser.iframePainel(self.financeiro, self.faturamento)
            self.browser.click('//*[@title="Novo faturamento..."]')
        except Exception as e:
            return self.message_error(f"Error clique Novo faturamento: {e}")

        # Regra de vencimento
        try:
            self.browser.iframeForm()
            self.browser.click('//div[@title="Selecione a regra de faturamento desejada."]/div/button')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                regra.descricao + Keys.ENTER
            )
            self.browser.click(f'//option[@value="{regra.id_web}"]')
        except Exception as e:
            return self.message_error(f"Error regra de vencimento: {e}")

        # data inicial
        try:
            self.browser.write(
                '//input[@title="Data de vencimento inicial das contas que devem ser faturadas."]',
                dia.strftime("%d%m%Y")
            )
        except Exception as e:
            return self.message_error(f"Error data inicial: {e}")

        # data final
        try:
            self.browser.write(
                '//input[@title="Data de vencimento final das contas que devem ser faturadas."]',
                (dia + timedelta(days=29)).strftime("%d%m%Y")
            )
        except Exception as e:
            return self.message_error(f"Error data final: {e}")

        # vencimento
        try:
            self.browser.write(
                '//input[@title="Data de vencimento da fatura que será criada."]',
                (dia + timedelta(days=8)).strftime("%d%m%Y")
            )
        except Exception as e:
            return self.message_error(f"Error vencimento: {e}")

        # clique confirma a geração
        try:
            self.browser.click('//input[@title="Clique para confirmar a geração da prévia de faturamento."]')
        except Exception as e:
            return self.message_error(f"Error clique confirma a geração: {e}")

        # clique executa filtro
        try:
            self.browser.click('//button[@title="Clique para executar o filtro deste novo faturamento."]')
            sleep(60)
        except Exception as e:
            return self.message_error(f"Error clique executa filtro: {e}")

        # alert concluir filtro
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(f"Error alert concluir filtro: {e}")

        # clique no filtro criado
        try:
            self.browser.iframeGridFaturamento(self.financeiro, self.faturamento)
            self.browser.dbclick('//div[@role="rowgroup"]/div/div')
        except Exception as e:
            return self.message_error(f"Error clique executa filtro: {e}")

        # clique seleção de todos
        try:
            self.browser.iframeGridRes(self.financeiro, self.faturamento)
            self.browser.click('//input[@id="rowselectAll"]')
        except Exception as e:
            return self.message_error(f"Error clique seleção de todos: {e}")

        # clique ignorar todas contas
        try:
            self.browser.iframePainel(self.financeiro, self.faturamento)
            self.browser.click('//button[@title="Ignorar contas para o faturamento."]')
        except Exception as e:
            return self.message_error(f"Error clique ignorar todas contas: {e}")

        # alert ignorar todas contas
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(f"Error alert ignorar todas contas: {e}")

        # clique desmarca seleção de todos
        try:
            self.browser.iframeGridRes(self.financeiro, self.faturamento)
            self.browser.click('//input[@id="rowselectAll"]')
        except Exception as e:
            return self.message_error(f"Error clique desmarcaseleção de todos: {e}")

        # seleção de profile
        try:
            self.browser.iframeGridRes(self.financeiro, self.faturamento)
            self.browser.write(
                '//td[@class=" webix_last_row" and @column="10"]/div/input',
                "Digital"
            )
        except Exception as e:
            return self.message_error(f"Error seleção de profile: {e}")

        # clique seleção de todos
        try:
            self.browser.iframeGridRes(self.financeiro, self.faturamento)
            self.browser.click('//input[@id="rowselectAll"]')
        except Exception as e:
            return self.message_error(f"Error clique seleção de todos: {e}")

        # clique reabilitar contas
        try:
            self.browser.iframePainel(self.financeiro, self.faturamento)
            self.browser.click('//button[@title="Reabilitar contas para o faturamento."]')
        except Exception as e:
            return self.message_error(f"Error clique reabilitar contas: {e}")

        # alert reabilitar contas
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(f"Error alert reabilitar contas: {e}")

        # clique remover inadimplência
        try:
            self.browser.iframePainel(self.financeiro, self.faturamento)
            self.browser.click(
                '//button[@title="Ferramenta para remover clientes com inadimplência deste faturamento."]'
            )
        except Exception as e:
            return self.message_error(f"Error clique remover inadimplência: {e}")

        # tempo de inadimplência
        try:
            self.browser.iframeForm()
            self.browser.write(
                '//input[@title="Informe a quantidade de dias de inadimplência de fatura, para que a regra desconsidere a fatura."]',
                "45"
            )
        except Exception as e:
            return self.message_error(f"Error tempo de inadimplência: {e}")

        # tempo de inadimplência
        try:
            self.browser.write(
                '//input[@title="Justifique o motivo desta ação."]',
                "Clientes com mais de 45 dias de inadimplência"
            )
        except Exception as e:
            return self.message_error(f"Error tempo de inadimplência: {e}")

        # clique processar ordem de inadimplência
        try:
            self.browser.click(
                '//button[@title="Clique para processar a ordem de suspensão de inadimplentes."]'
            )
            sleep(30)
        except Exception as e:
            return self.message_error(f"Error clique processar ordem de inadimplência: {e}")

        # alert tempo de inadimplência
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(f"Error alert tempo de inadimplência: {e}")

        return self.message_sucess("Success!")
