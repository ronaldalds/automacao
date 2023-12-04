import os
import time
from mk.coin.coin import Financeiro
from datetime import datetime
from mk.models import (
    Login,
    TipoOS,
    Profile,
    MotivoCancelamento,
    GrupoAtendimento,
)
# from dotenv import load_dotenv
from app.cancelamento.models import Cancelamento
from selenium.webdriver.common.keys import Keys
from mk.mk_drive import Mk
from mk.aside.aside_financeiro import PainelDoCliente
# from mk.mk_select import (
#     TIPO_DA_OS,
#     DEFEITO,
#     PROFILE_MK01,
#     PROFILE_MK03,
#     MOTIVO_DE_CANCELAMENTO_MK01,
#     MOTIVO_DE_CANCELAMENTO_MK03,
#     GRUPO_DE_ATENDIMENTO_MK01,
#     GRUPO_DE_ATENDIMENTO_MK03
# )

# load_dotenv()


class ProcessoCancelamento:
    def __init__(self, conexao: Cancelamento):
        self.__conexao = conexao
        self.__financeiro = Financeiro()
        self.__painel_do_cliente = PainelDoCliente()

    def _message_error(self, message) -> Cancelamento:
        error = f"ERROR;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.__conexao.observacao = f'{error};{message}'
        return self.__conexao

    def _message_sucess(self, message) -> Cancelamento:
        sucess = f"SUCESS;{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.__conexao.observacao = f'{sucess};{message}'
        return self.__conexao

    def _get_id(self, model, field) -> int:
        id: int = model.objects.get(
            descricao=field,
            mk=self.__conexao.mk
        ).id_web
        return id

    def _set_multa(self, browser: Mk) -> Cancelamento | None:
        try:
            id_profile = self._get_id(Profile, self.__conexao.profile)
            print(id_profile)
        except Exception as e:
            return self._message_error(f"Error: {e}")

        # clique editar contrato
        try:
            browser.iframePainel(self.__financeiro, self.__painel_do_cliente)
            browser.click('//*[@title="Alterar contrato"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error clique editar contrato: {e}")

        # clique contas associadas
        try:
            browser.iframeForm()
            browser.click('//button[@title="Contas associadas ao contrato"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error clique contas associadas: {e}")

        # clique inserir nova conta
        try:
            browser.click('//button[@title="Inserir nova conta no contrato."]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error clique inserir nova conta: {e}")

        # criar multa
        try:
            browser.iframeFormRes()
        except Exception as e:
            browser.close()
            return self._message_error(f"Error criar multa: {e}")

        # descricao da multa
        try:
            browser.write(
                '//*[@title="Descrição identificativa da conta."]',
                "Multa por rescisão contratual"
            )
        except Exception as e:
            browser.close()
            return self._message_error(f"Error descricao da multa: {e}")

        # valor da multa
        try:
            browser.write(
                '//*[@title="Valor do lançamento"]',
                self.__conexao.valor_multa
            )
        except Exception as e:
            browser.close()
            return self._message_error(f"Error valor da multa: {e}")

        # vencimento da multa
        try:
            browser.write(
                '//*[@title="Data de vencimento da conta."]',
                self.__conexao.data_vcto_multa_contratual
            )
        except Exception as e:
            browser.close()
            return self._message_error(f"Error vencimento da multa: {e}")

        # quantidade de parcelas
        try:
            browser.write('//*[@title="Número de parcela"]', 1)
        except Exception as e:
            browser.close()
            return self._message_error(f"Error quantidade de parcelas: {e}")

        # plano de contas
        try:
            id_plano_de_contas = self.__conexao.planos_de_contas.split()[0]
            browser.click('//*[@title="Unidade de plano de contas referenciada para o lançamento"]/div/button')
            browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{id_plano_de_contas}" + Keys.ENTER
            )
            browser.click(
                f'//option[@value="{id_plano_de_contas}"]'
            )
        except Exception as e:
            browser.close()
            return self._message_error(f"Error plano de contas: {e}")

        # próxima etapa da multa
        try:
            browser.click('//*[@title="Próxima etapa."]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error próxima etapa da multa: {e}")

        # faturar ?
        try:
            browser.click('//div[@title="Deseja faturar agora estas contas?\nMarcando SIM, será criada uma fatura 1/1 para cada conta inserida."]/div/button')
            browser.click('//option[@value="S"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error faturar ?: {e}")

        # qual profile usar
        try:
            browser.click(
                '//div[@title="Selecione a profile desejada"]/div/button'
            )
            browser.write(
                '//input[@id="lookupSearchQuery"]',
                f"{self.__conexao.profile.split()[0]}" + Keys.ENTER)
            browser.click(f'//option[@value="{id_profile}"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error qual profile usar: {e}")

        # marca check box
        try:
            browser.click('//input[@title="Marque essa opção para confirmar seu desejo de inserir a nova conta."]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error marca check box: {e}")

        # concluir multa
        try:
            browser.click('//button[@title="Clique para realizar a inserção"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error concluir multa: {e}")

        # fechar visualizar/Editar contrato
        try:
            browser.iframeMain()
            browser.click('//div[@class="OptionClose"]')
        except Exception as e:
            browser.close()
            return self._message_error(
                f"Error fechar visualizar/Editar contrato: {e}"
            )

        return None

    def cancelar(self) -> Cancelamento:
        try:
            id_tipo_os = self._get_id(TipoOS, self.__conexao.tipo_os)
            id_motivo_de_cancelamento = self._get_id(
                MotivoCancelamento, self.__conexao.motivo_cancelamento
            )
            id_grupo_atendimento = self._get_id(
                GrupoAtendimento, self.__conexao.id_grupo_atendimento
            )
            print(id_tipo_os)
            print(id_motivo_de_cancelamento)
            print(id_grupo_atendimento)
        except Exception as e:
            return self._message_error(f"Error: {e}")

        try:
            mk = Login.objects.get(mk=self.__conexao.mk)
            browser = Mk(
                username=mk.username,
                password=mk.password,
                url=mk.url,
            )
        except Exception as e:
            return self._message_error(f"Error instância: {e}")

        print(f"Iniciou MK:{mk.mk} Doc.: {self.__conexao.documento_codigo}")

        browser.login()

        # fechar tela de complete seu cadastro
        try:
            browser.iframeMain()
            browser.click('//div[@class="OptionClose"]')
        except Exception as e:
            print(f"Warning tela cadastro: {e}")

        # clique moeda financeiro
        try:
            browser.iframeCoin()
            browser.click(self.__financeiro.xpath())
        except Exception as e:
            browser.close()
            return self._message_error(f"Error clique moeda financeiro: {e}")

        # clique aside Painel do cliente
        try:
            browser.iframeAsideCoin(self.__financeiro)
            browser.click(self.__painel_do_cliente.xpath())
        except Exception as e:
            browser.close()
            return self._message_error(
                f"Error clique aside Painel do cliente: {e}"
            )

        # clique pesquisa avançada
        try:
            browser.iframePainel(self.__financeiro, self.__painel_do_cliente)
            browser.click('//*[@title="Clique para fazer uma pesquisa \
                avançada de clientes ou fornecedores"]')
        except Exception as e:
            browser.close()
            return self._message_error(f"Error clique pesquisa avançada: {e}")

        # pesquisar por Código de cadastro
        try:
            browser.iframeForm()
            browser.click('//*[@class="HTMLComboBox"]/div[2]/div')
            browser.write(
                '//input[@id="lookupSearchQuery"]',
                "C" + Keys.ENTER
            )
            browser.click('//option[@value="7"]')
            browser.write(
                '//input[@title="Código do cliente."]',
                self.__conexao.cod_pessoa
            )
            browser.click(
                '//button[@title="Clique para efetivar sua pesquisa."]'
            )
        except Exception as e:
            browser.close()
            return self._message_error(f"Error Código de cadastro: {e}")

        # clique no resultado de pesquisa avançada
        try:
            browser.iframeGridCancelamento(
                self.__financeiro,
                self.__painel_do_cliente
            )
            browser.dbclick(f'//div[text()={self.__conexao.cod_pessoa}]')
        except Exception as e:
            browser.close()
            return self._message_error(
                f"Error resultado de pesquisa avançada: {e}"
            )

        # clique duplo no cadastro do cliente
        try:
            browser.iframeGridRes(self.__financeiro, self.__painel_do_cliente)
            browser.click(f'//div[text()={self.__conexao.contrato}]')
        except Exception as e:
            browser.close()
            return self._message_error(
                f"Error clique duplo no cadastro do cliente: {e}"
            )

        # criar multa em caso do contrato ter multa
        if "S" in self.__conexao.incidencia_de_multa.upper():
            self._set_multa()

        time.sleep(5)
        browser.close()
        return None




        # # click no resultado do click duplo no cadastro do cliente
        # try:
        #     browser.iframeGridRes(financeiro, painel_do_cliente)
        #     browser.click(f'//div[text()={item.contrato}]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};click no resultado do click duplo no cadastro do cliente'
        #     return item

        # # click cancelar contrato
        # try:
        #     browser.iframePainel(financeiro, painel_do_cliente)
        #     browser.click('//*[@title="Cancelar contrato"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};click cancelar contrato'
        #     return item

        # # Motivo de cancelamento
        # try:
        #     browser.iframeForm()
        #     browser.click('//div[@title="Selecione um motivo de cancelamento."]/div/button')
        #     browser.write('//input[@id="lookupSearchQuery"]', "Inadi" + Keys.ENTER)
        #     browser.click(f'//option[@value="{motivo_de_cancelamento}"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Motivo de cancelamento'
        #     return item

        # # detalhes do motivo de cancelamento
        # try:
        #     browser.write('//textarea[@title="Informe detalhes do cancelamento do contrato."]', item.detalhes_cancelamento)
        # except:
        #     browser.close()
        #     item.observacao = f'{error};detalhes do motivo de cancelamento'
        #     return item

        # # proxima etapa do cancelar contrato 2
        # try:
        #     browser.click('//div[@class="HTMLTabContainer"]/div[2]/div[@class="next"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};proxima etapa do cancelar contrato 2'
        #     return item

        # # proxima etapa do cancelar contrato 3
        # try:
        #     browser.click('//div[@class="HTMLTabContainer"]/div[3]/div[@class="next"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};proxima etapa do cancelar contrato 3'
        #     return item
        
        # # checkbox Abrir O.S de retirada de equipamentos
        # try:
        #     browser.click('//*[@title="Marque esta opção, para que seja aberta uma O.S. de retirada de equipamentos para este cliente."]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};checkbox Abrir O.S de retirada de equipamentos'
        #     return item

        # # Tipo da O.S
        # try:
        #     browser.click('//div[@title="Informa qual o tipo da Ordem de Serviço."]/div/button')
        #     browser.write('//input[@id="lookupSearchQuery"]', item.tipo_os + Keys.ENTER)
        #     browser.click(f'//option[@value="{id_tipo_os}"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Tipo da O.S'
        #     return item

        # # Grupo de atendimento
        # try:
        #     browser.click('//div[@class="HTMLTabContainer"]/div[5]/div[7]/div[2]/div/button')
        #     browser.write('//input[@id="lookupSearchQuery"]', item.grupo_atendimento_os + Keys.ENTER)
        #     browser.click(f'//option[@value="{valor_grupo_atendimento}"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Grupo de atendimento'
        #     return item

        # # Defeito
        # try:
        #     browser.click('//div[@title="Neste campo é informado o defeito associado a esta Ordem de Serviço."]/div/button')
        #     browser.write('//input[@id="lookupSearchQuery"]', "C" + Keys.ENTER)
        #     browser.click(f'//option[@value="{DEFEITO["Cancelamento contratual"]}"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Defeito'
        #     return item

        # # Descrição da O.S.
        # try:
        #     browser.write('//textarea[@title="Descreva as informações para a sua O.S."]', item.relato_do_problema)
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Descrição da O.S.'
        #     return item

        # # proxima etapa do cancelar contrato
        # try:
        #     browser.click('//div[@class="HTMLTabContainer"]/div[5]/div[@class="next"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};proxima etapa do cancelar contrato'
        #     return item

        # # click checkbox cancelar contrato
        # try:
        #     browser.click(f'//div[@class="HTMLTabContainer"]/div[6]/div[17]/input[@type="checkbox"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};click checkbox cancelar contrato'
        #     return item
        
        # # Terminar cancelamento contrato
        # try:
        #     browser.click('//button[@title="Clique para finalizar"]')
        # except:
        #     browser.close()
        #     item.observacao = f'{error};Terminar cancelamento contrato'
        #     return item

        # # alert concluir cancelamento
        # try:
        #     browser.include()
        # except:
        #     browser.close()
        #     item.observacao = f'{error};alert concluir cancelamento'
        #     return item

        # time.sleep(5)
        # browser.close()
        # item.observacao = f'{sucess};cancelamento de contrato conluído'
        # item.status = True
        # return item
