from django.apps import AppConfig


class IndicadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.indicador'

    def ready(self) -> None:
        from utils.desk.drive import Desk
        from datetime import datetime
        from .models import Chamado
        from .models import Interacao
        from apscheduler.schedulers.background import BackgroundScheduler

        desk = Desk()

        def carga_chamado():
            chamados = desk.relatorio("140")
            print("Atualizando chamados...")
            if chamados:
                for chamado in chamados.get("root"):
                    item = Chamado.objects.filter(
                        id=chamado.get("CodChamado")
                    ).first()
                    if not item:
                        print(item)
                        data_criacao = datetime.strptime(
                            chamado.get("DataCriacao"),
                            "%d-%m-%Y"
                        )
                        data_finalizacao = datetime.strptime(
                            chamado.get("DataFinalizacao"),
                            "%d-%m-%Y"
                        )
                        data = Chamado(
                            id=chamado.get("CodChamado"),
                            data_criacao=data_criacao,
                            data_finalizacao=data_finalizacao,
                            assunto=chamado.get("Assunto"),
                            nome_categoria=chamado.get("NomeCategoria"),
                            total_horas_1_2_atendimento_str=chamado.get(
                                "TotalHorasPrimeiroSegundoAtendimento"
                            ),
                            nome_sla_status_atual=chamado.get(
                                "NomeSlaStatusAtual"
                            ),
                            sla_2_expirado=chamado.get("Sla2Expirado"),
                            first_call=chamado.get("FirstCall"),
                            nome_operador=chamado.get("NomeOperador"),
                            nome_status=chamado.get("NomeStatus"),
                        )
                        data.save()
                        print(chamado)

        def carga_interacao():
            interacoes = desk.relatorio("141")
            print("Atualizando interações...")
            if interacoes:
                for interacao in interacoes.get("root"):
                    chamado = Chamado.objects.filter(
                        id=interacao.get("NChamado")
                    ).first()
                    if chamado:
                        item = Interacao.objects.filter(
                            chamado=chamado.id,
                            seguencia=interacao.get("Sequencia")
                        ).first()
                        if not item:
                            data = Interacao(
                                chamado=chamado,
                                status_acao_nome_relatorio=interacao.get(
                                    "StatusAcaoNomeRelatorio"
                                ),
                                fantasia_fornecedor=interacao.get(
                                    "FantasiaFornecedor",
                                    ""
                                ),
                                seguencia=int(interacao.get("Sequencia")),
                            )
                            data.save()
                            print(interacao)

        sheduler = BackgroundScheduler(daemon=True)
        jobs = sheduler.get_jobs()
        if jobs:
            sheduler.shutdown()
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(carga_chamado, 'interval', minutes=12)
        sheduler.add_job(carga_interacao, 'interval', minutes=14)

        sheduler.start()
