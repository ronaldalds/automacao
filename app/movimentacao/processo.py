from .models import Movimentacao
from datetime import datetime
from utils.mk.coin.coin import Workspace
from utils.mk.aside.aside_workspace import OsPainel
from utils.mk.drive import Mk
from utils.mk.models import Login


class Movimentar:
    def __init__(self, os: Movimentacao):
        self.os = os
        self.workspace = Workspace()
        self.ospainel = OsPainel()
        self.browser: Mk
        self.login_mk: Login

    def message_error(self, message: str) -> None:
        error = f"ERROR;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.browser.close()
        self.os.observacao = f'{error};{message}'
        self.os.save()

    def message_sucess(self, message: str) -> None:
        sucess = f"SUCESS;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.browser.close()
        self.os.observacao = f'{sucess};{message}'
        self.os.status = True
        self.os.save()

    def movimentar(self):
        print(f"Iniciou movimentação O.S: {self.os.id}")
        try:
            self.login_mk = Login.objects.get(mk=self.os.mk)
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

        # clique moeda workspace
        try:
            self.browser.iframeCoin()
            self.browser.click(self.workspace.xpath())
        except Exception as e:
            return self.message_error(f"Error clique moeda Workspace: {e}")

        # clique aside O.S Painel
        try:
            self.browser.iframeAsideCoin(self.workspace)
            self.browser.click(self.ospainel.xpath())
        except Exception as e:
            return self.message_error(f"Error clique aside O.S Painel: {e}")

        # O.S Finalizadas
        try:
            self.browser.iframePainel(self.workspace, self.ospainel)
            self.browser.click('//span[text()="Finalizadas"]')
        except Exception as e:
            return self.message_error(f"Error O.S Finalizadas: {e}")

        # Movimentação de estoque
        try:
            self.browser.click('//*[@title="Movimentações de estoque com erros ou não qualificadas."]')
        except Exception as e:
            return self.message_error(f"Error Movimentação de estoque: {e}")

        # Mostrar movimentações
        try:
            self.browser.iframeGridInterna(self.workspace, self.ospainel)
            self.browser.click('//img[@id="imgFECTHALL"]')
        except Exception as e:
            return self.message_error(f"Error Mostrar movimentações: {e}")

        # Pesquisa Código
        try:
            self.browser.write('//td[@role="presentation" and @column="0"]/div/input', self.os.id)
        except Exception as e:
            return self.message_error(f"Error Pesquisa do Código: {e}")

        # Clique na O.S
        try:
            self.browser.click(f'//*[text()="{self.os.id}"]')
        except Exception as e:
            return self.message_error(f"Error Clique na O.S: {e}")

        # Gerar movimentação
        try:
            self.browser.iframePainel(self.workspace, self.ospainel)
            self.browser.click('//*[@title="Gerar movimento manual de estoque"]')
        except Exception as e:
            return self.message_error(f"Error Gerar movimentação: {e}")

        # Primeira tela movimentação
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@id="next1_btn_855515"]')
        except Exception as e:
            return self.message_error(f"Error Primeira tela movimentação: {e}")

        # Segunda tela movimentação
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@id="next2_btn_855526"]')
        except Exception as e:
            return self.message_error(f"Error Segunda tela movimentação: {e}")

        # checkbox terceira tela movimentação
        try:
            self.browser.iframeForm()
            self.browser.click(
                '//input[@title="Marque para dar ciência à movimentação do estoque" and @type="checkbox"]'
            )
        except Exception as e:
            return self.message_error(f"Error checkbox terceira tela movimentação: {e}")

        # Terceira tela movimentação
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@id="bt_fim_btn_855535"]')
        except Exception as e:
            return self.message_error(f"Error Terceira tela movimentação: {e}")

        self.message_sucess("Movimentação concluída")
