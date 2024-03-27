from django.apps import AppConfig


class FaturamentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.faturamento'

    def ready(self) -> None:
        from apscheduler.schedulers.background import BackgroundScheduler
        from .processo import FaturamentoProcesso

        sheuler_faturamento = BackgroundScheduler(deamon=True)
        jobs = sheuler_faturamento.get_jobs()
        if jobs:
            sheuler_faturamento.shutdown()

        mk_1 = FaturamentoProcesso(mk=1)
        # mk_3 = FaturamentoProcesso(mk=3)
        mk_1.regra()
        sheuler_faturamento.configure(timezone="america/fortaleza")
        # sheuler_faturamento.add_job(mk_1.regra, 'interval', minutes=0.1)
        # sheuler_faturamento.add_job(mk_3.regra, 'interval', minutes=0.1)
        sheuler_faturamento.start()
