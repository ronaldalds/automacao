from .models import Chamado, Interacao
from utils.desk.drive import Desk
from datetime import datetime


class CargaIndicadores:
    def __init__(self):
        self.desk = Desk()

    def chamados_desk(self):
        chamados = self.desk.relatorio("140")
        print(f"[{datetime.now()}] Atualizando chamados...")
        if not chamados:
            return
        for chamado in chamados:
            exists_chamado = Chamado.objects.filter(
                id=chamado.get("CodChamado")
            ).exists()
            andamento = chamado.get("DataFinalizacao") == "00-00-0000"
            if exists_chamado and andamento:
                item = Chamado.objects.filter(
                    id=chamado.get("CodChamado")
                ).first()
                item.nome_sla_status_atual = chamado.get("NomeSlaStatusAtual")
                item.sla_2_expirado = chamado.get("Sla2Expirado")
                item.first_call = chamado.get("FirstCall")
                item.nome_status = chamado.get("NomeStatus")
                item.sla_1_expirado = chamado.get("Sla1Expirado")
                item.total_horas_1_atendimento_str = chamado.get(
                    "TempoUtilAtPrimeiroAtendimento"
                )
                item.total_horas_1_2_atendimento_str = chamado.get(
                    "TotalHorasPrimeiroSegundoAtendimento"
                )
                item.nome_operador = chamado.get("NomeOperador", "")
                item.save()
            elif not exists_chamado:
                print(chamado)
                novo = Chamado()
                novo.id = chamado.get("CodChamado")
                novo.data_criacao = datetime.strptime(
                    chamado.get("DataCriacao"),
                    "%d-%m-%Y"
                )
                novo.andamento = andamento
                if not andamento:
                    novo.data_finalizacao = datetime.strptime(
                        chamado.get("DataFinalizacao"),
                        "%d-%m-%Y"
                    )
                novo.assunto = chamado.get("Assunto")
                novo.nome_categoria = chamado.get("NomeCategoria")
                novo.total_horas_1_2_atendimento_str = chamado.get(
                    "TotalHorasPrimeiroSegundoAtendimento"
                )
                novo.nome_sla_status_atual = chamado.get(
                    "NomeSlaStatusAtual"
                )
                novo.sla_2_expirado = chamado.get("Sla2Expirado")
                novo.first_call = chamado.get("FirstCall")
                novo.nome_operador = chamado.get("NomeOperador", "")
                novo.nome_status = chamado.get("NomeStatus")
                novo.sla_1_expirado = chamado.get("Sla1Expirado")
                novo.total_horas_1_atendimento_str = chamado.get(
                    "TempoUtilAtPrimeiroAtendimento"
                )
                novo.save()
        print(f"[{datetime.now()}] Finalizado chamados...")

    def interacao_desk(self):
        interacoes = self.desk.relatorio("141")
        print(f"[{datetime.now()}] Atualizando interações...")
        if not interacoes:
            return
        for interacao in interacoes:
            chamado = Chamado.objects.filter(
                id=interacao.get("NChamado")
            ).first()
            if not chamado:
                continue
            existe_interacao = Interacao.objects.filter(
                chamado=chamado.id,
                seguencia=interacao.get("Sequencia")
            ).exists()
            if existe_interacao:
                continue
            print(interacao)
            novo = Interacao()
            novo.chamado = chamado
            novo.status_acao_nome_relatorio = interacao.get(
                "StatusAcaoNomeRelatorio"
            )
            novo.fantasia_fornecedor = interacao.get(
                "FantasiaFornecedor",
                ""
            )
            novo.seguencia = interacao.get(
                "Sequencia"
            )
            novo.chamado_aprovadores = interacao.get(
                "ChamadoAprovadores",
                ""
            )
            novo.tempo_corrido_interacao_str = interacao.get(
                "TempoCorridoAcoes"
            )
            novo.save()
        print(f"[{datetime.now()}] Finalizado interações...")
