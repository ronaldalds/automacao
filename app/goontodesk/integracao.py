import re
from datetime import datetime
from utils.goon.drive import Goon
from utils.goon.models import StatusGoon
from utils.desk.drive import Desk
from utils.desk.models import StatusDesk, FormaAtendimentoDesk
from .models import OsGoon, StatusInfo


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


class GoonToDesk():
    def get_os_goon(self):
        try:
            go_on = Goon()
            data = datetime.now()
            chamado_desk = re.compile("[#][0-9]{4}[-][0-9]{6}")

            response = go_on.get_all_located_orders_by_agent(
                agente_codigo=0,
                mobile_agent="Internal",
                data=data
            )

            if not response:
                return

            for os in response["FormAnswers"]["FormAnswer"]:
                os_goon = OsGoon.objects.filter(
                    numero_os=int(os["NumeroOS"])
                ).first()
                if not os_goon:
                    data_os_goon = OsGoon(
                        numero_os=int(os["NumeroOS"]),
                        descricao=os["Descricao"],
                        tipo_servico=os["ExternalTipoServicoID"]
                    )
                    if bool(chamado_desk.search(os["Descricao"])):
                        descricao = chamado_desk.search(
                            os["Descricao"]
                        ).group()
                        data_os_goon.ordem_servico_externa = descricao.replace(
                            '#',
                            ''
                        )
                    data_os_goon.save()

                infos = os["StatusSequence"]["StatusInfo"]
                status_infos = StatusInfo.objects.filter(
                    os_goon=os_goon
                )
                goon = OsGoon.objects.filter(
                    numero_os=int(os["NumeroOS"])
                ).first()

                for c, status in enumerate(infos, 1):
                    data_info = status_infos.filter(sequencia=c).first()
                    if not data_info:
                        status_info = StatusInfo(
                            sequencia=c,
                            status=status.get("Status"),
                            data=status.get("DataHora"),
                            mobile_agent=status.get("MobileAgentName"),
                            mobile_phone=status.get("MobileAgentPhone"),
                            os_goon=goon,
                            enviado=False,
                        )
                        status_info.save()

        except Exception as e:
            print(f"Error get os goon: {e}")

    def set_chamado_desk(self, os_goon):
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

                # momento da criação "Qui, 20 de Julho de 2023 às 14:37"
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
                    forma_atendimento=query_forma_atendimento_desk.id,
                    cod_status=query_status_desk.id,
                    operador=operador,
                    horario=horario,
                    descricao=str_status
                )

        except Exception as e:
            print(f"Error set_chamado_desk: {e}")

    def goon_to_desk(self):
        data = datetime.now()
        print(data, 'goon to desk')
        res = self.get_os_goon(data, 10)
        if res:
            for ocorrencia in res:
                self.set_chamado_desk(ocorrencia)
