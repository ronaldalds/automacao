import re
from datetime import datetime, timedelta
from time import sleep
from goon.go_on_drive import Goon
from goon.models import StatusGoon
from desk.models import StatusDesk, FormaAtendimentoDesk
from desk.desk_drive import Desk


STATUS_GOON = {
    'DESP': 'Despachado',
    'AGEN': 'Agendado',
    'ACTE': 'Recebido pelo Agente',
    'TACM': 'Agente a caminho',
    'CCLI': 'Cancelado pelo cliente',
    'COPE': 'Cancelado pelo operador',
    'CTEC': 'Cancelado pelo agente',
    'INIC': 'Em Atendimento',
    'FIOK1': 'Pausado',
    'DESP2': 'Despachado',
    'ACTE2': 'Recebido pelo Agente',
    'FIOK': 'Finalizado',
}

STATUS_DESK = {
   "Agendamento": "000004",
   "Andamento": "000006",
   "Cancelado": "000003",
   "Resolvido": "000002"
}

FORMA_ATENDIMENTO_DESK = {
   "Desk Manager": "000009",
   "Acesso Remoto": "000001",
   "Whatsapp": "000051"
}

DIAS_SEMANA = {
    0: "Seg",
    1: "Ter",
    2: "Qua",
    3: "Qui",
    4: "Sex",
    5: "Sáb",
    6: "Dom"
}

MESES_ANO = [
    None,
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]


def get_os_goon(horario, atraso):
    try:
        go_on = Goon()

        horario_inicial = horario - timedelta(minutes=atraso)
        horario_final = horario
        data_to_desk = []

        response = go_on.get_all_located_orders_by_agent(
            agente_codigo=0,
            mobile_agent="Internal",
            data=horario
        )

        if not response:
            return data_to_desk

        chamado_desk = re.compile("[#][0-9]{4}[-][0-9]{6}")

        for os in response:
            if bool(chamado_desk.search(os["Descricao"])):
                os["StatusSequence"] = [att for att in os["StatusSequence"] if horario_inicial <= datetime.strptime(att["DataHora"], "%d/%m/%Y %H:%M:%S") <= horario_final]
                if os["StatusSequence"]:
                    descricao = chamado_desk.search(os["Descricao"]).group()
                    os["chamadoDesk"] = descricao.replace('#', '')
                    data_to_desk.append(os)

        return data_to_desk

    except Exception as e:
        print(f"Error get os goon: {e}")
        return data_to_desk


def set_chamado_desk(os_goon):
    try:
        # instancia objeto Desk
        desk = Desk()

        # id do chamado no desk
        chamado_desk = os_goon["chamadoDesk"]

        # descrição da O.S
        descricao = os_goon["Descricao"].replace(f"#{chamado_desk}", '')
        str_descricao = f"Descrição: {descricao}"

        # id os no go.on
        numero_os = f"OS Go.On: {os_goon['NumeroOS']}"

        # operador para interagir no chamado do desk
        operador = desk.operador_do_chamado(chamado_desk)

        if not operador:
            return

        # itera em quantos status acumulado tem para interagir no desk
        for status in os_goon["StatusSequence"]:
            # transforma a string data em objeto datetime
            data_hora = status["DataHora"]
            horario = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S")

            # dia da semana string
            dia_semana = DIAS_SEMANA[horario.weekday()]

            # dia do mes int
            dia_mes = horario.day

            # mes do ano string
            mes = MESES_ANO[horario.month]

            # ano int
            ano = horario.year

            # hora e minuto str
            hora = horario.strftime("%H:%M")

            # situação do chamado no momento
            query_situacao = StatusGoon.objects.get(
                nome=status['Status']
            )
            situacao = f"Status: {query_situacao.descricao}"

            # agente designado para a OS no go.on
            if status["MobileAgentName"]:
                agente = f"Agente: {status['MobileAgentName']}"
            else:
                agente = "Agente: Sem Agente designado"

            # momento da criação do status "Qui, 20 de Julho de 2023 às 14:37"
            momento = f"{dia_semana}, {dia_mes} de {mes} de {ano} às {hora}"

            str_conteudo = f"{str_descricao}\n{situacao}\n{agente}"

            str_status = f"{momento}\n{numero_os}\n{str_conteudo}"

            query_status_desk = StatusDesk.objects.get(
                nome="Andamento"
            )

            query_forma_atendimento_desk = FormaAtendimentoDesk.objects.get(
                nome="Desk Manager"
            )
            # interagir com o chamado
            desk.interagir_chamado(
                chamado_desk=chamado_desk,
                forma_atendimento=query_forma_atendimento_desk.descricao,
                cod_status=query_status_desk.descricao,
                operador=operador,
                horario=horario,
                descricao=str_status
            )

    except Exception as e:
        print(f"Error set_chamado_desk: {e}")


def goon_to_desk():
    while True:
        sleep(1)
        data = datetime.now()
        tempo_ciclo = 5
        proxima_data = data + timedelta(minutes=tempo_ciclo)
        str_data = data.strftime("%d/%m/%Y %H:%M")
        str_proixma_data = proxima_data.strftime("%d/%m/%Y %H:%M")
        if str_data == str_proixma_data:
            res = get_os_goon(data, tempo_ciclo)
            if res:
                for ocorrencia in res:
                    set_chamado_desk(ocorrencia)
