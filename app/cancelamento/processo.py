from datetime import datetime
from .models import Cancelamento
from selenium.webdriver.common.keys import Keys
from utils.mk.drive import Mk
from utils.mk.coin.coin import Financeiro
from utils.mk.aside.aside_financeiro import PainelDoCliente
from utils.mk.models import (
    Login,
    TipoOS,
    MotivoCancelamento,
    GrupoAtendimento,
    Defeito,
    Profile,
)


class Cancelar:
    def __init__(self, conexao: Cancelamento):
        self.conexao = conexao
        self.financeiro = Financeiro()
        self.painel_do_cliente = PainelDoCliente()
        self.browser: Mk
        self.login_mk: Login

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

    def cancelar(self) -> None:
        print(
            f"Iniciou Contrato.: {self.conexao.contrato}"
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
            self.id_motivo_de_cancelamento = MotivoCancelamento.objects.get(
                descricao=self.conexao.motivo_cancelamento,
                mk=self.conexao.mk
            ).id_web
            self.id_grupo_atendimento_os = GrupoAtendimento.objects.get(
                descricao=self.conexao.grupo_atendimento_os,
                mk=self.conexao.mk
            ).id_web
            self.id_defeito = Defeito.objects.get(
                descricao=self.conexao.defeito,
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

        # clique moeda financeiro
        try:
            self.browser.iframeCoin()
            self.browser.click(self.financeiro.xpath())
        except Exception as e:
            return self.message_error(f"Error clique moeda financeiro: {e}")

        # clique aside Painel do cliente
        try:
            self.browser.iframeAsideCoin(self.financeiro)
            self.browser.click(self.painel_do_cliente.xpath())
        except Exception as e:
            return self.message_error(f"Error clique aside Painel do cliente: {e}")

        # clique pesquisa avançada
        try:
            self.browser.iframePainel(self.financeiro, self.painel_do_cliente)
            self.browser.click('//*[@title="Clique para fazer uma pesquisa avançada de clientes ou fornecedores"]')
        except Exception as e:
            return self.message_error(f"Error clique pesquisa avançada: {e}")

        # pesquisar por Código de cadastro
        try:
            self.browser.iframeForm()
            self.browser.click('//*[@class="HTMLComboBox"]/div[2]/div')
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                "C" + Keys.ENTER
            )
            self.browser.click('//option[@value="7"]')
            self.browser.write(
                '//input[@title="Código do cliente."]',
                self.conexao.cod_pessoa
            )
            self.browser.click(
                '//button[@title="Clique para efetivar sua pesquisa."]'
            )
        except Exception as e:
            return self.message_error(f"Error Código de cadastro: {e}")

        # clique no resultado de pesquisa avançada
        try:
            self.browser.iframeGrid(
                self.financeiro,
                self.painel_do_cliente
            )
            self.browser.dbclick(f'//div[text()={self.conexao.cod_pessoa}]')
        except Exception as e:
            return self.message_error(f"Error resultado de pesquisa avançada: {e}")

        # clique duplo no cadastro do cliente
        try:
            self.browser.iframeGridRes(
                self.financeiro,
                self.painel_do_cliente
            )
            self.browser.click(f'//div[text()={self.conexao.contrato}]')
        except Exception as e:
            return self.message_error(
                f"Error clique duplo no cadastro do cliente: {e}"
            )

        # criar multa em caso do contrato ter multa
        if "S" in self.conexao.incidencia_de_multa.upper():
            self.set_multa()

        # clique no resultado do click duplo no cadastro do cliente
        try:
            self.browser.iframeGridRes(self.financeiro, self.painel_do_cliente)
            self.browser.click(f'//div[text()={self.conexao.contrato}]')
        except Exception as e:
            return self.message_error(
                f"Error clique no resultado do click duplo: {e}"
            )

        # clique cancelar contrato
        try:
            self.browser.iframePainel(self.financeiro, self.painel_do_cliente)
            self.browser.click('//*[@title="Cancelar contrato"]')
        except Exception as e:
            return self.message_error(
                f"Error clique cancelar contrato: {e}"
            )

        # Motivo de cancelamento
        try:
            self.browser.iframeForm()
            self.browser.click(
                '//div[@title="Selecione um motivo de cancelamento."\
                    ]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                self.conexao.motivo_cancelamento.split()[0] + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.id_motivo_de_cancelamento}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Motivo de cancelamento: {e}"
            )

        # detalhes do motivo de cancelamento
        try:
            self.browser.write(
                '//textarea[@title=\
                    "Informe detalhes do cancelamento do contrato."]',
                self.conexao.detalhes_cancelamento
            )
        except Exception as e:
            return self.message_error(
                f"Error detalhes do motivo de cancelamento: {e}"
            )

        # proxima etapa do cancelar contrato 2
        try:
            self.browser.click(
                '//div[@class="HTMLTabContainer"]/div[2]/div[@class="next"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error proxima etapa do cancelar contrato 2: {e}"
            )

        # proxima etapa do cancelar contrato 3
        try:
            self.browser.click(
                '//div[@class="HTMLTabContainer"]/div[3]/div[@class="next"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error proxima etapa do cancelar contrato 3: {e}"
            )

        # checkbox Abrir O.S de retirada de equipamentos
        try:
            self.browser.click(
                '//*[@title="Marque esta opção, para que seja aberta uma O.S. de retirada de equipamentos para este cliente."]'
            )
        except Exception as e:
            return self.message_error(
                f"Error checkbox Abrir O.S de retirada de equipamentos: {e}"
            )

        # Tipo da O.S
        try:
            self.browser.click(
                '//div[@title="Informa qual o tipo da Ordem de Serviço."]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                self.conexao.tipo_os.split()[0] + Keys.ENTER
            )
            self.browser.click(f'//option[@value="{self.id_tipo_os}"]')
        except Exception as e:
            return self.message_error(
                f"Error Tipo da O.S: {e}"
            )

        # Grupo de atendimento
        try:
            self.browser.click(
                '//div[@class="HTMLTabContainer"]/div[5]/div[7]/div[2]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                self.conexao.grupo_atendimento_os + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{self.id_grupo_atendimento_os}"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error Grupo de atendimento: {e}"
            )

        # Defeito
        try:
            self.browser.click(
                '//div[@title="Neste campo é informado o defeito associado a esta Ordem de Serviço."]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                self.conexao.defeito + Keys.ENTER
            )
            self.browser.click(f'//option[@value="{self.id_defeito}"]')
        except Exception as e:
            return self.message_error(
                f"Error Defeito: {e}"
            )

        # Descrição da O.S.
        try:
            self.browser.write(
                '//textarea[@title="Descreva as informações para a sua O.S."]',
                self.conexao.relato_do_problema
            )
        except Exception as e:
            return self.message_error(
                f"Error Descrição da O.S.: {e}"
            )

        # proxima etapa do cancelar contrato
        try:
            self.browser.click(
                '//div[@class="HTMLTabContainer"]/div[5]/div[@class="next"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error proxima etapa do cancelar contrato: {e}"
            )

        # clique checkbox cancelar contrato
        try:
            self.browser.click(
                '//div[@class="HTMLTabContainer"]/div[6]/div[19]/input[@type="checkbox"]'
            )
        except Exception as e:
            return self.message_error(
                f"Error clique checkbox cancelar contrato: {e}"
            )

        # Terminar cancelamento contrato
        try:
            self.browser.click('//button[@title="Clique para finalizar"]')
        except Exception as e:
            return self.message_error(
                f"Error Terminar cancelamento contrato: {e}"
            )

        # alert concluir cancelamento
        try:
            self.browser.include()
        except Exception as e:
            return self.message_error(
                f"Error alert concluir cancelamento: {e}"
            )

        self.message_sucess("cancelamento de contrato conluído")

    def set_multa(self) -> None:
        try:
            self.id_profile = Profile.objects.get(
                descricao=self.conexao.profile,
                mk=self.conexao.mk
            ).id_web
        except Exception as e:
            return self.message_error(f"Error: {e}")

        # clique editar contrato
        try:
            self.browser.iframePainel(self.financeiro, self.painel_do_cliente)
            self.browser.click('//*[@title="Alterar contrato"]')
        except Exception as e:
            return self.message_error(f"Error clique editar contrato: {e}")

        # clique contas associadas
        try:
            self.browser.iframeForm()
            self.browser.click(
                '//button[@title="Contas associadas ao contrato"]'
            )
        except Exception as e:
            return self.message_error(f"Error clique contas associadas: {e}")

        # clique inserir nova conta
        try:
            self.browser.click(
                '//button[@title="Inserir nova conta no contrato."]'
            )
        except Exception as e:
            return self.message_error(f"Error clique inserir nova conta: {e}")

        # criar multa
        try:
            self.browser.iframeFormRes()
        except Exception as e:
            return self.message_error(f"Error criar multa: {e}")

        # descricao da multa
        try:
            self.browser.write(
                '//*[@title="Descrição identificativa da conta."]',
                "Multa por rescisão contratual"
            )
        except Exception as e:
            return self.message_error(f"Error descricao da multa: {e}")

        # valor da multa
        try:
            self.browser.write(
                '//*[@title="Valor do lançamento"]',
                str(self.conexao.valor_multa.to_integral_value())
            )
        except Exception as e:
            return self.message_error(f"Error valor da multa: {e}")

        # vencimento da multa
        try:
            self.browser.write(
                '//*[@title="Data de vencimento da conta."]',
                self.conexao.data_vcto_multa_contratual.replace("/", "")
            )
        except Exception as e:
            return self.message_error(f"Error vencimento da multa: {e}")

        # quantidade de parcelas
        try:
            self.browser.write('//*[@title="Número de parcela"]', 1)
        except Exception as e:
            return self.message_error(f"Error quantidade de parcelas: {e}")

        # plano de contas
        try:
            id_plano_de_contas = self.conexao.planos_de_contas.split()[0]
            self.browser.click(
                '//*[@title="Unidade de plano de contas referenciada para o lançamento"]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{id_plano_de_contas}" + Keys.ENTER
            )
            self.browser.click(
                f'//option[@value="{id_plano_de_contas}"]'
            )
        except Exception as e:
            return self.message_error(f"Error plano de contas: {e}")

        # próxima etapa da multa
        try:
            self.browser.click('//*[@title="Próxima etapa."]')
        except Exception as e:
            return self.message_error(f"Error próxima etapa da multa: {e}")

        # faturar ?
        try:
            self.browser.click(
                '//div[@title="Deseja faturar agora estas contas?\nMarcando SIM, será criada uma fatura 1/1 para cada conta inserida."]/div/button'
            )
            self.browser.click('//option[@value="S"]')
        except Exception as e:
            return self.message_error(f"Error faturar ?: {e}")

        # qual profile usar
        try:
            self.browser.click(
                '//div[@title="Selecione a profile desejada"]/div/button'
            )
            self.browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.conexao.profile.split()[0]}" + Keys.ENTER)
            self.browser.click(f'//option[@value="{self.id_profile}"]')
        except Exception as e:
            return self.message_error(f"Error qual profile usar: {e}")

        # marca check box
        try:
            self.browser.click(
                '//input[@title="Marque essa opção para confirmar seu desejo de inserir a nova conta."]'
            )
        except Exception as e:
            return self.message_error(f"Error marca check box: {e}")

        # concluir multa
        try:
            self.browser.click(
                '//button[@title="Clique para realizar a inserção"]'
            )
        except Exception as e:
            return self.message_error(f"Error concluir multa: {e}")

        # fechar visualizar/Editar contrato
        try:
            self.browser.iframeMain()
            self.browser.click('//div[@class="OptionClose"]')
        except Exception as e:
            return self.message_error(
                f"Error fechar visualizar/Editar contrato: {e}"
            )