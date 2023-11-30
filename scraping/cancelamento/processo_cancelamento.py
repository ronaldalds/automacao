import os
import time
from datetime import datetime
from mk.models import (
    Login,
    TipoOS,
    Profile,
)
# from dotenv import load_dotenv
from app.cancelamento.models import Cancelamento
from selenium.webdriver.common.keys import Keys
from mk.mk_drive import Mk
from mk.coin.coin import Financeiro
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


def message(
    item: Cancelamento,
    tipo: bool,
    msg: str
) -> Cancelamento:
    horario = datetime.now().strftime("%d/%m/%Y %H:%M")
    error = f"ERROR;{horario}"
    sucess = f"SUCESS;{horario}"
    if tipo:
        item.observacao = f'{sucess};{msg}'
    else:
        item.observacao = f'{error};{msg}'
    return item


def cancelamento(item: Cancelamento) -> Cancelamento:
    print(f'Iniciou MK:{item.mk} Documento: {item.documento_codigo}')
    try:
        mk = Login.objects.get(mk=item.mk)
        browser = Mk(
            username=mk.username,
            password=mk.password,
            url=mk.url,
        )
    except Exception as e:
        return message(
            item=item,
            tipo=False,
            msg=f"Error instância: {e}"
        )

    try:
        id_tipo_os = TipoOS.objects.get(
            descricao=item.tipo_os,
            mk=item.mk
        ).id_web
        print(id_tipo_os)
    except Exception as e:
        browser.close()
        return message(
            item=item,
            tipo=False,
            msg=f"Error Tipode O.S: {e}"
        )

    try:
        profile = Profile.objects.get(
            descricao="Boleto Digital - Santander",
            mk=item.mk
        ).id_web
        print(profile)
    except Exception as e:
        browser.close()
        return message(
            item=item,
            tipo=False,
            msg=f"Error Profile: {e}"
        )
    # motivo_de_cancelamento  = MOTIVO_DE_CANCELAMENTO_MK01["Inadimplência"]
    # valor_grupo_atendimento = GRUPO_DE_ATENDIMENTO_MK01[item.grupo_atendimento_os]
    # time.sleep(5)
    browser.close()
    return None
    # if item.mk == 1:
    #     browser = Mk(
    #         username=os.getenv('USERNAME_MK'),
    #         password=os.getenv('PASSWORD_MK'),
    #         url=os.getenv('URL_MK1'),
    #     )
    #     profile = PROFILE_MK01["Boleto Digital - Santander"]
    #     motivo_de_cancelamento  = MOTIVO_DE_CANCELAMENTO_MK01["Inadimplência"]
    #     valor_grupo_atendimento = GRUPO_DE_ATENDIMENTO_MK01[item.grupo_atendimento_os]
    # elif item.mk == 3:
    #     browser = Mk(
    #         username=os.getenv('USERNAME_MK3'),
    #         password=os.getenv('PASSWORD_MK3'),
    #         url=os.getenv('URL_MK3'),
    #     )
    #     profile = PROFILE_MK03['Boleto Digital - Bradesco']
    #     motivo_de_cancelamento  = MOTIVO_DE_CANCELAMENTO_MK03["Inadimplência"]
    #     valor_grupo_atendimento = GRUPO_DE_ATENDIMENTO_MK03[item.grupo_atendimento_os]

    # else:
    #     return message(
    #         browser=browser,
    #         item=item,
    #         tipo=False,
    #         msg="Não foi possível criar instancia do mk."
    #     )

    # financeiro = Financeiro()
    # painel_do_cliente = PainelDoCliente()

    # browser.login()

    # # fechar tela de complete seu cadastro
    # try:
    #     browser.iframeMain()
    #     browser.click('//div[@class="OptionClose"]')
    # except:
    #     pass
    
    # # click na moeda financeiro
    # try:
    #     browser.iframeCoin()
    #     browser.click(financeiro.xpath())
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click na moeda financeiro.'
    #     return item

    # # click aside Painel do cliente
    # try:
    #     browser.iframeAsideCoin(financeiro)
    #     browser.click(painel_do_cliente.xpath())
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click aside Painel do cliente.'
    #     return item

    # # click pesquisa avançada
    # try:
    #     browser.iframePainel(financeiro, painel_do_cliente)
    #     browser.click('//*[@title="Clique para fazer uma pesquisa avançada de clientes ou fornecedores"]')
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click pesquisa avançada.'
    #     return item

    # # pesquisar por Código de cadastro
    # try:
    #     browser.iframeForm()
    #     browser.click('//*[@class="HTMLComboBox"]/div[2]/div')
    #     browser.write('//input[@id="lookupSearchQuery"]', "C" + Keys.ENTER)
    #     browser.click('//option[@value="7"]')
    #     browser.write('//input[@title="Código do cliente."]', item.cod_pessoa)
    #     browser.click('//button[@title="Clique para efetivar sua pesquisa."]')
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click pesquisa avançada.'
    #     return item
    
    # # click no resultado de pesquisa avançada
    # try:
    #     browser.iframeGridCancelamento(financeiro, painel_do_cliente)
    #     browser.dbclick(f'//div[text()={item.cod_pessoa}]')
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click no resultado de pesquisa avançada'
    #     return item

    # # click no resultado do click duplo no cadastro do cliente
    # try:
    #     browser.iframeGridRes(financeiro, painel_do_cliente)
    #     browser.click(f'//div[text()={item.contrato}]')
    # except:
    #     browser.close()
    #     item.observacao = f'{error};click no resultado do click duplo no cadastro do cliente'
    #     return item

    # # criar multa em caso do contrato ter multa
    # if "S" in item.incidencia_de_multa.upper():
    #     # click no botão editar contrato
    #     try:
    #         browser.iframePainel(financeiro, painel_do_cliente)
    #         browser.click('//*[@title="Alterar contrato"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};click no botão editar contrato'
    #         return item

    #     # click no botão contas associadas
    #     try:
    #         browser.iframeForm()
    #         browser.click('//button[@title="Contas associadas ao contrato"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};click no botão contas associadas'
    #         return item

    #     # click inserir nova conta
    #     try:
    #         browser.click('//button[@title="Inserir nova conta no contrato."]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};click inserir nova conta'
    #         return item

    #     # criar multa
    #     try:
    #         browser.iframeFormRes()
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};criar multa'
    #         return item

    #     # descricao da multa
    #     try:
    #         browser.write('//*[@title="Descrição identificativa da conta."]', "Multa por rescisão contratual")
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};descricao da multa'
    #         return item

    #     # valor da multa
    #     try:
    #         browser.write('//*[@title="Valor do lançamento"]', item.valor_multa)
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};valor da multa'
    #         return item

    #     # vencimento da multa
    #     try:
    #         browser.write('//*[@title="Data de vencimento da conta."]', item.data_vcto_multa_contratual)
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};vencimento da multa'
    #         return item

    #     # quantidade de parcelas
    #     try:
    #         browser.write('//*[@title="Número de parcela"]', 1)
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};quantidade de parcelas'
    #         return item

    #     # plano de contas
    #     try:
    #         browser.click('//*[@title="Unidade de plano de contas referenciada para o lançamento"]/div/button')
    #         browser.write('//input[@id="lookupSearchQuery"]', f"{item.planos_de_contas.split()[0]}" + Keys.ENTER)
    #         browser.click(f'//option[@value="{item.planos_de_contas.split()[0]}"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};plano de contas'
    #         return item

    #     # próxima etapa da multa
    #     try:
    #         browser.click('//*[@title="Próxima etapa."]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};próxima etapa da multa'
    #         return item

    #     # faturar ?
    #     try:
    #         browser.click('//div[@title="Deseja faturar agora estas contas?\nMarcando SIM, será criada uma fatura 1/1 para cada conta inserida."]/div/button')
    #         browser.click('//option[@value="S"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};faturar ?'
    #         return item

    #     # qual profile usar
    #     try:
    #         browser.click('//div[@title="Selecione a profile desejada"]/div/button')
    #         browser.write('//input[@id="lookupSearchQuery"]', "B" + Keys.ENTER)
    #         browser.click(f'//option[@value="{profile}"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};qual profile usar'
    #         return item

    #     # marca check box
    #     try:
    #         browser.click('//input[@title="Marque essa opção para confirmar seu desejo de inserir a nova conta."]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};marca check box'
    #         return item

    #     # concluir multa
    #     try:
    #         browser.click('//button[@title="Clique para realizar a inserção"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};concluir multa'
    #         return item

    #     # fechar visualizar/Editar contrato
    #     try:
    #         browser.iframeMain()
    #         browser.click('//div[@class="OptionClose"]')
    #     except:
    #         browser.close()
    #         item.observacao = f'{error};fechar visualizar/Editar contrato'
    #         return item

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
