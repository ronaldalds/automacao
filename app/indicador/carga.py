from utils.desk.drive import Desk
from .models import Chamado, Interacao
from datetime import datetime


class CargaIndicadores:
    def __init__(self):
        self.desk = Desk()

    def tempo_atendimento(self, tempo: str) -> float | None:
        if tempo in ["0", "00:00:00"]:
            return 0.0 if tempo == "0" else None
        negative = "-" in tempo
        if negative:
            tempo = tempo.replace("-", "")
        horas, minutos, segundos = map(int, tempo.split(':'))
        total = horas + minutos / 60 + segundos / 3600
        return round(total * (-1 if negative else 1), 2)

    def chamado_save(self, chamado: Chamado, data: dict) -> None:
        chamado.nome_categoria = data.get("NomeCategoria", "")
        chamado.assunto = data.get("Assunto", "")
        chamado.nome_status = data.get("NomeStatus", "")
        chamado.nome_operador = data.get("NomeOperador", "")
        chamado.sla_1_expirado = data.get("Sla1Expirado", "")
        chamado.sla_2_expirado = data.get("Sla2Expirado", "")
        chamado.first_call = data.get("FirstCall")
        chamado.nome_sistema = data.get("_203471", "")
        chamado.nome_sla_status_atual = data.get("NomeSlaStatusAtual", "")
        chamado.tempo_restante_1 = self.tempo_atendimento(str(data.get("TempoRestantePrimeiroAtendimento")))
        chamado.tempo_restante_2 = self.tempo_atendimento(str(data.get("TempoRestanteSegundoAtendimento")))
        chamado.total_horas_1_atendimento = self.tempo_atendimento(
            str(data.get("TempoUtilAtPrimeiroAtendimento"))
        )
        chamado.total_horas_1_2_atendimento = self.tempo_atendimento(
            str(data.get("TotalHorasPrimeiroSegundoAtendimento"))
        )
        chamado.nome_grupo = data.get("NomeGrupo", "")
        chamado.save()

    def interacao_save(self, interacao: Interacao, data: dict) -> None:
        interacao.seguencia = data.get("Sequencia")
        interacao.status_acao_nome_relatorio = data.get(
            "StatusAcaoNomeRelatorio",
        )
        interacao.fantasia_fornecedor = data.get("FantasiaFornecedor", "")
        interacao.chamado_aprovadores = data.get("ChamadoAprovadores", "")
        interacao.tempo_corrido_interacao = self.tempo_atendimento(
            str(data.get("TempoCorridoAcoes"))
        )
        interacao.save()

    def chamados_desk(self):
        response = self.desk.relatorio("140")
        print(f"[{datetime.now()}] Atualizando chamados...")
        if not response:
            return
        for data in response:
            item = Chamado.objects.filter(
                id=data.get("CodChamado")
            ).first()
            andamento = data.get("DataFinalizacao") == "00-00-0000"
            if item and not andamento:
                item.andamento = andamento
                item.data_finalizacao = datetime.strptime(
                    data.get("DataFinalizacao"),
                    "%d-%m-%Y"
                )
                self.chamado_save(item, data)
            elif item and andamento:
                self.chamado_save(item, data)
            elif not item:
                print(data)
                novo = Chamado()
                novo.id = data.get("CodChamado")
                novo.data_criacao = datetime.strptime(
                    data.get("DataCriacao"),
                    "%d-%m-%Y"
                )
                novo.andamento = andamento
                if not andamento:
                    novo.data_finalizacao = datetime.strptime(
                        data.get("DataFinalizacao"),
                        "%d-%m-%Y"
                    )
                self.chamado_save(novo, data)
        print(f"[{datetime.now()}] Finalizado chamados...")

    def interacao_desk(self):
        response = self.desk.relatorio("141")
        print(f"[{datetime.now()}] Atualizando interações...")
        if not response:
            return
        for data in response:
            chamado = Chamado.objects.filter(
                id=data.get("NChamado")
            ).first()
            if not chamado:
                continue
            existe_interacao = Interacao.objects.filter(
                chamado=chamado.id,
                seguencia=data.get("Sequencia")
            ).exists()
            if not existe_interacao:
                print(data)
                novo = Interacao()
                novo.chamado = chamado
                self.interacao_save(novo, data)
        print(f"[{datetime.now()}] Finalizado interações...")
