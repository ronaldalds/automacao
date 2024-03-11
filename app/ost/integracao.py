import time
import telebot
from datetime import datetime
from utils.mkat.drive import Mkat
from utils.telegram.models import UserTelegram, BotTelegram
from .models import (
    TipoOs,
    TempoSla,
    InformacaoOs,
    Log,
    TecnicoMensagem,
    ErrorOs,
)


class Notificacao:
    def informacaoes(self, tipo_os) -> list[InformacaoOs]:
        tipo = TipoOs.objects.filter(tipo=tipo_os).first()
        informacao = InformacaoOs.objects.filter(
            id_tipo_os=tipo
        )
        if informacao:
            return informacao
        else:
            return InformacaoOs.objects.filter(
                id_tipo_os=TipoOs.objects.filter(tipo="PADRAO").first().pk
            )

    def verificar_agenda_os(self) -> None:
        mkat = Mkat()
        agendamentos = mkat.agenda_os()
        for agenda in agendamentos:
            ordem_servico: dict = agenda.get("os", {})
            encerrado: bool = ordem_servico.get("encerrado", False)
            operador: str = ordem_servico.get(
                "operador_abertura",
                "Sem Operador"
            )
            if not encerrado and (operador != "bot.sistemas"):
                self.verificar_os(ordem_servico)

    def verificar_os(self, ordem_servico: dict) -> None:
        bot_telegram = telebot.TeleBot(
            BotTelegram.objects.filter(nome="TELEGRAM_OST").first().token,
            parse_mode=None
        )
        grupo = UserTelegram.objects.filter(
            nome="GRUPO_NOTIFICACAO_OST"
        ).first().id
        tipo_os: dict = ordem_servico.get("tipo_os", {})
        motivo: str = ordem_servico.get("motivo", "")
        descricao_tipo_os: str = tipo_os.get("descricao", "PADRAO")
        informacoes_os = self.informacaoes(descricao_tipo_os)
        cod = ordem_servico.get('cod', '')
        operador_abertura = ordem_servico.get('operador_abertura', '')
        for detalhes in informacoes_os:
            msg_os = f"OS {cod} - {descricao_tipo_os}."
            msg_operador = f"Operador {operador_abertura}."
            msg_detalhe = f"Falta detalhe ({detalhes.nome}) no motivo da O.S."
            msg = f"🔴 🟡 🟢\n\n{msg_os}\n{msg_operador}\n{msg_detalhe}"
            if detalhes.nome.replace(":", "") not in motivo:
                if not ErrorOs.objects.filter(
                    os=ordem_servico.get('cod', ''),
                    tipo=descricao_tipo_os,
                    operador=ordem_servico.get('operador_abertura', ''),
                    detalhe=detalhes.nome
                ).exists():
                    error = ErrorOs(
                        os=ordem_servico.get('cod', ''),
                        tipo=descricao_tipo_os,
                        operador=ordem_servico.get('operador_abertura', ''),
                        detalhe=detalhes.nome
                    )
                    error.save()
                bot_telegram.send_message(
                    chat_id=grupo,
                    text=msg
                )
                time.sleep(7)

    def sla_os(self, Tipo_OS) -> int:
        tipo = TipoOs.objects.filter(tipo=Tipo_OS, status=True).first()
        if tipo:
            return tipo.sla
        else:
            return -1

    def tempo_de_aviso(self) -> list:
        tempo_aviso = TempoSla.objects.all()
        return sorted([x.sla for x in tempo_aviso], reverse=True)

    def notificar(
        self,
        Cod_OS,
        ID_Tecnico,
        Tempo_Aviso,
        Nome_Tecnico: str,
        Tipo_OS,
        data_abertura: datetime,
    ) -> None:
        mensagens = TecnicoMensagem.objects.filter(
            nome_tecnico=Nome_Tecnico,
            cod_os=Cod_OS,
            chat_id=ID_Tecnico,
            sla=Tempo_Aviso,
            status=True
        )
        bot_telegram = telebot.TeleBot(
            BotTelegram.objects.filter(nome="TELEGRAM_OST").first().token,
            parse_mode=None
        )
        horario = data_abertura.strftime("%d/%m/%Y %H:%M")
        Nome_Tecnico_Formatado = Nome_Tecnico.replace('.', ' ').title()
        msg_1 = f"🔴 🟡 🟢\n\nOlá {Nome_Tecnico_Formatado}."
        msg_2 = f"Falta menos de {Tempo_Aviso} "
        msg_3 = "horas para a seguinte O.S. expirar."
        msg_4 = f"Cód O.S. : {Cod_OS}"
        msg_5 = f"Tipo O.S : {Tipo_OS}"
        msg_6 = f"Data Abertura : {horario}"
        msg = f"{msg_1}\n\n\r{msg_2}{msg_3}\n\n\r{msg_4}\n{msg_5}\n{msg_6}"
        if not mensagens.exists():
            print(msg)
            tm = TecnicoMensagem(
                nome_tecnico=Nome_Tecnico,
                chat_id=ID_Tecnico,
                mensagem=msg,
                sla=Tempo_Aviso,
                cod_os=Cod_OS,
            )
            try:
                bot_telegram.send_message(
                    chat_id=ID_Tecnico,
                    text=msg
                )

                tm.status = True
                tm.save()
            except Exception:
                bot_telegram.send_message(
                    chat_id=UserTelegram.objects.filter(
                        nome="ADMINISTRADOR"
                    ).first().id,
                    text=msg
                )
                tm.status = False
                tm.save()
            time.sleep(7)

    def diferenca_hora(self, data_abertura: datetime):
        agora = datetime.now()
        diferenca = agora - data_abertura
        return diferenca.total_seconds() / 3600

    def shedule_api(self):
        print('Rodando : ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        Lista_Tecnicos = UserTelegram.objects.filter(
            funcao=1,
            status=True
        )
        for tecnico in Lista_Tecnicos:
            print(f"id: {tecnico.id} Nome: {tecnico.nome}")
            mkat = Mkat()
            agenda_Tecnico = mkat.agenda_tecnico(tecnico.nome)
            tempo_aviso = self.tempo_de_aviso()
            for agenda in agenda_Tecnico:
                data_obj = datetime.strptime(
                    agenda['os']['data_abertura'],
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                hora_obj = datetime.strptime(
                    agenda['os']['hora_abertura'].split(".")[0],
                    "%H:%M:%S"
                )
                horario_abertura = data_obj.replace(
                    hour=hora_obj.hour,
                    minute=hora_obj.minute,
                    second=hora_obj.second,
                    microsecond=hora_obj.microsecond
                )
                Encerrado = agenda['os']['encerrado']
                Cod_OS = agenda['codos']
                Tipo_OS = agenda['os']['tipo_os']['descricao']

                if not Encerrado:
                    hora_passada = self.diferenca_hora(horario_abertura)
                    sla_max = self.sla_os(Tipo_OS)

                    if sla_max > 0:
                        for aviso in tempo_aviso:
                            sla_1 = (sla_max - hora_passada) >= 0
                            sla_2 = (sla_max - hora_passada) <= aviso
                            if sla_1 and sla_2:
                                self.notificar(
                                    Cod_OS,
                                    tecnico.id,
                                    aviso,
                                    tecnico.nome,
                                    Tipo_OS,
                                    horario_abertura
                                )
                                Log.objects.create()
