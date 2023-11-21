import time
import os
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from mk.mk_driver import Mk
from mk.coin.coin import Financeiro
from mk.aside.aside_financeiro import PainelDoCliente
from mk.mk_select import (
    TIPO_DA_OS,
    DEFEITO,
    CHECK_BOX_CANCELAR_MK01,
    CHECK_BOX_CANCELAR_MK03,
    PROFILE_MK01,
    PROFILE_MK03,
    MOTIVO_DE_CANCELAMENTO_MK01,
    MOTIVO_DE_CANCELAMENTO_MK03,
    GRUPO_DE_ATENDIMENTO_MK01,
    GRUPO_DE_ATENDIMENTO_MK03
)

load_dotenv()

def cancelamento(
        mk,
        cod_pessoa,
        contrato,
        detalhes_cancelamento,
        tipo_da_os,
        grupo_atendimento_os,
        relato_do_problema,
        # dados para multa
        incidencia_multa,
        valor_multa,
        vencimento_multa,
        planos_contas
        ):
    hora = datetime.now()
    print(f'Iniciou cancelamento {hora.strftime("%d/%m/%Y %H:%M")} MK:{mk:02} código:{cod_pessoa} contrato:{contrato} grupo:{grupo_atendimento_os} multa:{valor_multa}')
    error = f"\033[91mERROR\033[0m;CANCELAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
    warning = f"\033[93mWARNING\033[0m;CANCELAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"
    sucess = f"\033[92mSUCESS\033[0m;CANCELAMENTO;{hora.strftime('%d/%m/%Y %H:%M')}"

    prefixo_log_cancelamento = f'MK:{mk};código:{cod_pessoa};contrato:{contrato}'

    valor_tipo_de_os = TIPO_DA_OS[tipo_da_os]
    if mk == 1:
        instance = Mk(
            username=os.getenv('USERNAME_MK1'),
            password=os.getenv('PASSWORD_MK1'),
            url=os.getenv('URL_MK1'),
        )
        profile = PROFILE_MK01["Boleto Digital - Santander"]
        motivo_de_cancelamento  = MOTIVO_DE_CANCELAMENTO_MK01["Inadimplência"]
        valor_grupo_atendimento = GRUPO_DE_ATENDIMENTO_MK01[grupo_atendimento_os]
        div_cancelar = CHECK_BOX_CANCELAR_MK01["Cancelar"]
    elif mk == 3:
        instance = Mk(
            username=os.getenv('USERNAME_MK3'),
            password=os.getenv('PASSWORD_MK3'),
            url=os.getenv('URL_MK3'),
        )
        profile = PROFILE_MK03['Boleto Digital - Bradesco']
        motivo_de_cancelamento  = MOTIVO_DE_CANCELAMENTO_MK03["Inadimplência"]
        valor_grupo_atendimento = GRUPO_DE_ATENDIMENTO_MK03[grupo_atendimento_os]
        div_cancelar = CHECK_BOX_CANCELAR_MK03["Cancelar"]

    else:
        print(f'{error};{prefixo_log_cancelamento};Não foi possível criar instancia do mk...')
        return f'{error};{prefixo_log_cancelamento};Não foi possível criar instancia do mk...'

    financeiro = Financeiro()
    painel_do_cliente = PainelDoCliente()

    instance.login()

    # try:
    #     instance.minimizeChat()
    # except:
    #     pass

    # fechar tela de complete seu cadastro
    try:
        instance.iframeMain()
        instance.click('//div[@class="OptionClose"]')
    except:
        pass
    
    # click na moeda financeiro
    instance.iframeCoin()
    instance.click(financeiro.xpath())

    # click aside Painel do cliente
    instance.iframeAsideCoin(financeiro)
    instance.click(painel_do_cliente.xpath())

    # click pesquisa avançada
    instance.iframePainel(financeiro, painel_do_cliente)
    instance.click('//*[@title="Clique para fazer uma pesquisa avançada de clientes ou fornecedores"]')

    # pesquisar por Código de cadastro
    instance.iframeForm()
    instance.click('//*[@class="HTMLComboBox"]/div[2]/div')
    instance.write('//input[@id="lookupSearchQuery"]', "C" + Keys.ENTER)
    instance.click('//option[@value="7"]')
    instance.write('//input[@title="Código do cliente."]', cod_pessoa)
    instance.click('//button[@title="Clique para efetivar sua pesquisa."]')
    
    # click no resultado de pesquisa avançada
    try:
        instance.iframeGridCancelamento(financeiro, painel_do_cliente)
        instance.dbclick(f'//div[text()={cod_pessoa}]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};click no resultado de pesquisa avançada')
        return f'{error};{prefixo_log_cancelamento};click no resultado de pesquisa avançada'

    # click no resultado do click duplo no cadastro do cliente
    try:
        instance.iframeGridRes(financeiro, painel_do_cliente)
        instance.click(f'//div[text()={contrato}]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};click no resultado do click duplo no cadastro do cliente')
        return f'{error};{prefixo_log_cancelamento};click no resultado do click duplo no cadastro do cliente'
    
    # criar multa em caso do contrato ter multa
    if incidencia_multa:
        # click no botão editar contrato
        try:
            instance.iframePainel(financeiro, painel_do_cliente)
            instance.click('//*[@title="Alterar contrato"]')
        except:
            instance.close()
            print(f'{error};{prefixo_log_cancelamento};click no botão editar contrato')
            return f'{error};{prefixo_log_cancelamento};click no botão editar contrato'

        # click no botão contas associadas
        instance.iframeForm()
        instance.click('//button[@title="Contas associadas ao contrato"]')

        # click inserir nova conta
        instance.click('//button[@title="Inserir nova conta no contrato."]')

        # criar multa
        instance.iframeFormRes()

        # descricao da multa
        instance.write('//*[@title="Descrição identificativa da conta."]', "Multa por rescisão contratual")

        # valor da multa
        instance.write('//*[@title="Valor do lançamento"]', valor_multa)
        
        # vencimento da multa
        try:
            instance.write('//*[@title="Data de vencimento da conta."]', vencimento_multa)
        except:
            instance.close()
            print(f'{error};{prefixo_log_cancelamento};vencimento da multa')
            return f'{error};{prefixo_log_cancelamento};vencimento da multa'

        # quantidade de parcelas
        instance.write('//*[@title="Número de parcela"]', 1)

        # plano de contas
        try:
            instance.click('//*[@title="Unidade de plano de contas referenciada para o lançamento"]/div/button')
            instance.write('//input[@id="lookupSearchQuery"]', f"{planos_contas.split()[0]}" + Keys.ENTER)
            instance.click(f'//option[@value="{planos_contas.split()[0]}"]')
        except:
            instance.close()
            print(f'{error};{prefixo_log_cancelamento};plano de contas')
            return f'{error};{prefixo_log_cancelamento};plano de contas'

        # próxima etapa da multa
        instance.click('//*[@title="Próxima etapa."]')

        # faturar ?
        instance.click('//div[@title="Deseja faturar agora estas contas?\nMarcando SIM, será criada uma fatura 1/1 para cada conta inserida."]/div/button')
        instance.click('//option[@value="S"]')

        # qual profile usar
        instance.click('//div[@title="Selecione a profile desejada"]/div/button')
        instance.write('//input[@id="lookupSearchQuery"]', "B" + Keys.ENTER)
        instance.click(f'//option[@value="{profile}"]')

        # marca check box
        instance.click('//input[@title="Marque essa opção para confirmar seu desejo de inserir a nova conta."]')

        # concluir multa
        instance.click('//button[@title="Clique para realizar a inserção"]')

        # fechar visualizar/Editar contrato
        instance.iframeMain()
        instance.click('//div[@class="OptionClose"]')

        # click no resultado do click duplo no cadastro do cliente
    
    # click no resultado do click duplo no cadastro do cliente
    try:
        instance.iframeGridRes(financeiro, painel_do_cliente)
        instance.click(f'//div[text()={contrato}]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};click no resultado do click duplo no cadastro do cliente')
        return f'{error};{prefixo_log_cancelamento};click no resultado do click duplo no cadastro do cliente'

    # click cancelar contrato
    try:
        instance.iframePainel(financeiro, painel_do_cliente)
        instance.click('//*[@title="Cancelar contrato"]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};click cancelar contrato')
        return f'{error};{prefixo_log_cancelamento};click cancelar contrato'

    # Motivo de cancelamento
    instance.iframeForm()
    instance.click('//div[@title="Selecione um motivo de cancelamento."]/div/button')
    instance.write('//input[@id="lookupSearchQuery"]', "Inadi" + Keys.ENTER)
    instance.click(f'//option[@value="{motivo_de_cancelamento}"]') 

    # detalhes do motivo de cancelamento
    instance.write('//textarea[@title="Informe detalhes do cancelamento do contrato."]', detalhes_cancelamento)

    # proxima etapa do cancelar contrato
    instance.click('//div[@class="HTMLTabContainer"]/div[2]/div[@class="next"]')

    # proxima etapa do cancelar contrato
    instance.click('//div[@class="HTMLTabContainer"]/div[3]/div[@class="next"]')
    
    # checkbox Abrir O.S de retirada de equipamentos
    instance.click('//*[@title="Marque esta opção, para que seja aberta uma O.S. de retirada de equipamentos para este cliente."]')

    # Tipo da O.S
    try:
        instance.click('//div[@title="Informa qual o tipo da Ordem de Serviço."]/div/button')
        instance.write('//input[@id="lookupSearchQuery"]', tipo_da_os + Keys.ENTER)
        instance.click(f'//option[@value="{valor_tipo_de_os}"]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};Tipo da O.S')
        return f'{error};{prefixo_log_cancelamento};Tipo da O.S'

    # Grupo de atendimento
    try:
        instance.click('//div[@class="HTMLTabContainer"]/div[5]/div[7]/div[2]/div/button')
        instance.write('//input[@id="lookupSearchQuery"]', grupo_atendimento_os + Keys.ENTER)
        instance.click(f'//option[@value="{valor_grupo_atendimento}"]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};Grupo de atendimento')
        return f'{error};{prefixo_log_cancelamento};Grupo de atendimento'

    # Defeito
    instance.click('//div[@title="Neste campo é informado o defeito associado a esta Ordem de Serviço."]/div/button')
    instance.write('//input[@id="lookupSearchQuery"]', "C" + Keys.ENTER)
    instance.click(f'//option[@value="{DEFEITO["Cancelamento contratual"]}"]')

    # Descrição da O.S.
    instance.write('//textarea[@title="Descreva as informações para a sua O.S."]', relato_do_problema)

    # proxima etapa do cancelar contrato
    instance.click('//div[@class="HTMLTabContainer"]/div[5]/div[@class="next"]')

    # click checkbox cancelar contrato
    try:
        instance.click(f'//div[@class="HTMLTabContainer"]/div[6]/div[{div_cancelar}]/input[@type="checkbox"]')
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};click checkbox cancelar contrato')
        return f'{error};{prefixo_log_cancelamento};click checkbox cancelar contrato'
    
    # Terminar cancelamento contrato
    instance.click('//button[@title="Clique para finalizar"]')

    # alert concluir cancelamento
    try:
        instance.include()
    except:
        instance.close()
        print(f'{error};{prefixo_log_cancelamento};alert para concluir')
        return f'{error};{prefixo_log_cancelamento};alert para concluir'

    time.sleep(5)
    instance.close()
    print(f'{sucess};{prefixo_log_cancelamento};cancelamento de contrato conluído')
    return f'{sucess};{prefixo_log_cancelamento};cancelamento de contrato conluído'
