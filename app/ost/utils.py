"""Module Notifications for scheduler"""
from datetime import datetime, timedelta
import time
import requests
import telebot
from dotenv import dotenv_values
from .models import SlaOS
from .models import TipoOS
from .models import TempoSLA
from .models import InformacaoOS
from .models import Tecnico
from .models import Log
from .models import TecnicoMensagem

env = dotenv_values(".env")


class Notificacao:
    def __init__(self):
        self.__url_agenda_tecnico = "https://mkat.online.psi.br/agenda/tecnico"
        self.__url_agenda_os = "https://mkat.online.psi.br/agenda/os"
        self.__auth = env.get("TOKEN_MKAT")
        self.__bot_telegram = telebot.TeleBot(env.get("BOT_TOKEN_TELEGRAM_OST"), parse_mode=None)

    def agenda_os(self):
        data_json = {
            "token": self.__auth,
            "de": datetime.now().strftime('%Y-%m-%d'),
            "ate": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            "mk": 1
        }

        try:
            response = requests.post(
                self.__url_agenda_os,
                json=data_json,
            )

        except:
            print("Error na request da rota agenda os")
            time.sleep(60)
            self.agenda_os()
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error na resposta da rota agenda os")
            time.sleep(60)
            self.agenda_os()

    def informacaoes(self, tipo_os) -> list[dict]:
        tipo = TipoOS.objects.filter(tipo=tipo_os).first()
        tipo_padrao = TipoOS.objects.filter(tipo="PADRÃO").first()
        informacao = InformacaoOS.objects.filter(id_tipo_os=tipo).values("nome")
        if informacao:
            return informacao
        else:
            return InformacaoOS.objects.filter(id_tipo_os=tipo_padrao).values("nome")

    def verificar_agenda_os(self) -> None:
        agendamentos = self.agenda_os()
        for agenda in agendamentos:
            ordem_servico: dict = agenda.get("os", {})
            encerrado: bool = ordem_servico.get("encerrado", False)
            operador: str = ordem_servico.get("operador_abertura", "Sem Operador")
            if not encerrado and (operador != "bot.sistemas"):
                self.verificar_os(ordem_servico)

    def verificar_os(self, ordem_servico: dict) -> None:
        tipo_os: dict = ordem_servico.get("tipo_os", {})
        motivo: str = ordem_servico.get("motivo", "")
        descricao_tipo_os: str = tipo_os.get("descricao", "PADRÃO")
        informacoes_os: list = self.informacaoes(tipo_os=descricao_tipo_os)
        
        for detalhes in informacoes_os:
            if detalhes.get("nome").replace(":", "") not in motivo:
                print(f"{ordem_servico.get('cod')} - {descricao_tipo_os} - {detalhes}")
                msg_os = f"OS {ordem_servico.get('cod', '')} - {descricao_tipo_os}."
                msg_operador = f"Operador {ordem_servico.get('operador_abertura', '')}."
                msg_detalhe = f"Falta detalhe ({detalhes.get('nome')}) no motivo da O.S."
                msg = f"🔴 🟡 🟢\n\n{msg_os}\n{msg_operador}\n{msg_detalhe}"
                self.__bot_telegram.send_message(chat_id=int(env.get("CHAT_ID_GRUPO_NOTIFICACAO_OST")), text=msg)
                time.sleep(5)


    def agenda_tecnico(self, tecnico) -> list[dict]:
        data_json = {
            "token": self.__auth,
            "tecnico": tecnico,
            "de": datetime.now().strftime('%Y-%m-%d'),
            "ate": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            "mk": 1
        }

        try:
            response = requests.post(
                self.__url_agenda_tecnico,
                json=data_json,
            )
        except:
            print("Error na request da rota relatário")
            time.sleep(60)
            self.agenda_tecnico(tecnico)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error na resposta da rota agenda técnico")
            time.sleep(60)
            self.agenda_tecnico(tecnico)

    def sla_os(self, Tipo_OS) -> int:
        tipo = TipoOS.objects.filter(tipo=Tipo_OS).first()
        status=SlaOS.objects.filter(id_tipo_os=tipo, status=True).first()
        if status:
            return status.sla
        else:
            return -1

    def tempo_de_aviso(self) -> list:
        tempo_aviso = TempoSLA.objects.all().values("sla")
        return sorted([x.get("sla") for x in tempo_aviso], reverse=True)

    def notificar(self, Cod_OS, ID_Tecnico, Tempo_Aviso, Nome_Tecnico: str, Tipo_OS, Data_Abertura, Chat_ID: int) -> None:
        Mensagens = TecnicoMensagem.objects.filter(cod_os=Cod_OS, chat_id=ID_Tecnico, sla=Tempo_Aviso, status=True).values()

        if len(Mensagens) == 0:
            print('Nome_Tecnico : ', Nome_Tecnico)
            Nome_Tecnico_Formatado = Nome_Tecnico.replace('.', ' ').title()
            msg = f"🔴 🟡 🟢\n\nOlá {Nome_Tecnico_Formatado}.\n\n\rFalta menos de {Tempo_Aviso} horas para a seguinte O.S. expirar.\n\n\rCód O.S. : {Cod_OS}\nTipo O.S : {Tipo_OS}\nData Abertura : {Data_Abertura}"
            print(msg)
            try:
                self.__bot_telegram.send_message(chat_id=int(Chat_ID), text=msg)
                print(Chat_ID)

                TecnicoMensagem.objects.create(chat_id=Tecnico.objects.get(nome=Nome_Tecnico),
                                                mensagem=msg,
                                                sla=Tempo_Aviso,
                                                cod_os=Cod_OS,
                                                status=True
                                                )

            except:
                TecnicoMensagem.objects.create(
                    chat_id=Tecnico.objects.get(nome=Nome_Tecnico),
                    mensagem=msg,
                    sla=Tempo_Aviso,
                    cod_os=Cod_OS,
                    status=False)
                self.__bot_telegram.send_message(
                    chat_id=int(env.get("CHAT_ID_ADM")),
                    text=msg
                )

    def diferenca_hora(self, Data_Abertura):
        formato_data_hora = '%Y/%m/%d %H:%M:%S'
        data_e_hora_em_texto = datetime.now().strftime(formato_data_hora)

        return round(((datetime.strptime(data_e_hora_em_texto, formato_data_hora) -
                    datetime.strptime(Data_Abertura, formato_data_hora)).total_seconds())/3600, 2)

    def shedule_api(self):
        print('Rodando : ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        Lista_Tecnicos = Tecnico.objects.filter(status=True).values()

        for tecnico in Lista_Tecnicos:
            print('id : ', tecnico['id'],' Nome : ', tecnico['nome'], ' Chat_ID : ', tecnico['chat_id'])
            Chat_ID = tecnico['chat_id']
            Agenda_Tecnico = self.agenda_tecnico(tecnico['nome'])
            Tempo_Aviso = self.tempo_de_aviso()

            for agenda in Agenda_Tecnico:
                Data_Abertura = (agenda['os']['data_abertura'][:10]).replace(
                    '-', '/')+' '+agenda['os']['hora_abertura'][:8]
                Encerrado = agenda['os']['encerrado']
                Cod_OS = agenda['codos']
                Tipo_OS = agenda['os']['tipo_os']['descricao']

                if not Encerrado:
                    Hora_Passada = self.diferenca_hora(Data_Abertura)
                    Sla_Max = self.sla_os(Tipo_OS)

                    if Sla_Max > 0:
                        for tempo_aviso in Tempo_Aviso:
                            if ((Sla_Max - Hora_Passada) >= 0) and ((Sla_Max - Hora_Passada) <= tempo_aviso):
                                self.notificar(Cod_OS, tecnico['id'], tempo_aviso, tecnico['nome'], Tipo_OS, Data_Abertura, Chat_ID)
                                break
        Log.objects.create()
