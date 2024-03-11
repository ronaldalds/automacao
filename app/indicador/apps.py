from django.apps import AppConfig


class IndicadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.indicador'

    def ready(self) -> None:
        from apscheduler.schedulers.background import BackgroundScheduler
        from .carga import CargaIndicadores

        carga = CargaIndicadores()
        sheduler: BackgroundScheduler = BackgroundScheduler(daemon=True)
        jobs = sheduler.get_jobs()
        if jobs:
            sheduler.shutdown()
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(carga.chamados_desk, 'interval', minutes=9)
        sheduler.add_job(carga.interacao_desk, 'interval', minutes=5)

        sheduler.start()
