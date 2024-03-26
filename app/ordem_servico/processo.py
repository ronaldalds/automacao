import re
from time import sleep
from datetime import datetime
from .models import OrdemServico
from selenium.webdriver.common.keys import Keys
from utils.mk.coin.coin import Workspace
from utils.mk.aside.aside_workspace import OsPainel
from utils.mk.drive import Mk
from utils.mk.models import (
    Login,
    TipoOS,
    NivelSLA,
    GrupoAtendimento,
)


class Ordem:
    def __init__(self, conexao: OrdemServico):
        self.conexao = conexao
        self.workspace = Workspace()
        self.ospainel = OsPainel()
        self.browser: Mk
        self.login_mk: Login

    def documento(self, doc: str):
        rg_cpf = re.compile(
            "[0-9]{3}[.][0-9]{3}[.][0-9]{3}[-][0-9]{2}"
        )
        rg_cnpj = re.compile(
            "[0-9]{2}[.][0-9]{3}[.][0-9]{3}[/][0-9]{4}[-][0-9]{2}"
        )
        cpf = rg_cpf.search(doc)
        cnpj = rg_cnpj.search(doc)
        if cpf:
            return cpf.group()
        elif cnpj:
            return cnpj.group()
        else:
            return None

    def message_error(self, message: str) -> None:
        error = f"ERROR;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.browser.close()
        self.conexao.processamento = False
        self.conexao.observacao = f'{error};{message}'
        self.conexao.save()

    def message_sucess(self, message: str) -> None:
        sucess = f"SUCESS;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.browser.close()
        self.conexao.processamento = False
        self.conexao.observacao = f'{sucess};{message}'
        self.conexao.status = True
        self.conexao.save()

    def os(self):
        print(
            f"Iniciou documento.: {self.conexao.documento}"
        )
        try:
            self.login_mk = Login.objects.get(mk=self.conexao.mk)
            self.browser = Mk(
                username=self.login_mk.username,
                password=self.login_mk.password,
                url=self.login_mk.url,
            )
            self.browser.login()

        except Exception as e:
            return self.message_error(f"Error instância: {e}")

        try:
            self.id_tipo_os = TipoOS.objects.get(
                descricao=self.conexao.tipo_os,
                mk=self.conexao.mk
            ).id_web
            self.id_nivel_sla = NivelSLA.objects.get(
                descricao=self.conexao.nivel_sla,
                mk=self.conexao.mk
            ).id_web
            self.id_grupo_atendimento_os = GrupoAtendimento.objects.get(
                descricao=self.conexao.grupo_atendimento_os,
                mk=self.conexao.mk
            ).id_web

        except Exception as e:
            return self.message_error(f"Error: {e}")

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

        # Criar nova O.S
        try:
            self.browser.iframePainel(self.workspace, self.ospainel)
            self.browser.click('//*[@title="Criar Nova O.S."]')
        except Exception as e:
            return self.message_error(f"Error Criar nova O.S: {e}")

        # Identificador O.S Nome / Documento / Código
        try:
            self.browser.iframeForm()
            self.browser.click(
                '//*[@title="Este campo informa qual é o cliente associado a esta Ordem de Serviço."]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.documento(self.conexao.documento)}" + Keys.ENTER)
            self.browser.click(f'//option[@value="{self.conexao.cod_pessoa}"]')
        except Exception as e:
            return self.message_error(
                f"Error Identificador O.S Nome / Documento / Código: {e}"
            )

        # Avançar no assistente de O.S primeira tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[2]//button[@title="Avançar no assistente de O.S."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S primeira tela: {e}"
            )

        # Escolha de conexão Conexão Associada
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@title="Neste campo é informado para qual conexão foi aberta esta Ordem de Serviço."]/div/button')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.conexao.conexao_associada}" + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.conexao.conexao_associada}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Escolha de conexão Conexão Associada: {e}"
            )

        # Escolha nivel de SLA se habilitado
        try:
            sleep(5)
            self.browser.iframeForm()
            self.browser.click('//*[@title="Escolhe o nível de prioridade deste serviço."]/div/button')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.conexao.nivel_sla}" + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.id_nivel_sla}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Escolha nivel de SLA se habilitado: {e}"
            )

        # Avançar no assistente de O.S segunda tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[3]//button[@title="Avançar no assistente de O.S."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S segunda tela: {e}"
            )

        # Escolha tipo de O.S
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@title="Informa qual o tipo da Ordem de Serviço."]/div/button')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.conexao.tipo_os}" + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.id_tipo_os}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Escolha tipo de O.S: {e}"
            )

        # Escrever Relato do problema
        try:
            self.browser.iframeForm()
            self.browser.write(
                '//textarea[@title="Neste campo é informado o relato do cliente perante a abertura da Ordem de Serviço."]',
                f"{self.conexao.detalhes_os}" + Keys.ENTER
            )
        except Exception as e:
            return self.message_error(
                f"Error Escrever Relato do problema: {e}"
            )

        # Avançar no assistente de O.S terceira tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[4]//button[@title="Avançar no assistente de O.S."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S terceira tela: {e}"
            )

        # Avançar no assistente de O.S quarta tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[8]//button[@title="Avançar no assistente de O.S."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S quarta tela: {e}"
            )

        # Escolha Grupo de atendimento
        try:
            self.browser.iframeForm()
            self.browser.click('//div[@class="HTMLTabContainer"]/div[9]//div[@class="HTMLLookup"]/div[2]/div/button')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.conexao.grupo_atendimento_os}" + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.id_grupo_atendimento_os}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Escolha Grupo de atendimento: {e}"
            )

        # Avançar no assistente de O.S quinta tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[9]//button[@title="Avançar no assistente de O.S."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S quinta tela: {e}"
            )

        # Avançar no assistente de O.S sexta tela
        try:
            self.browser.click('//div[@class="HTMLTabContainer"]/div[10]//button[@title="Clique para efetivar a criação desta O.S.."]')
        except Exception as e:
            return self.message_error(
                f"Error Avançar no assistente de O.S sexta tela: {e}"
            )

        # alert concluir O.S
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(
                f"Error alert concluir O.S: {e}"
            )

        self.message_sucess("O.S do contrato conluído")
