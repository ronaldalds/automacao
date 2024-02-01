from django.apps import AppConfig


# Importe o modelo Ativado do seu aplicativo
class OstConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.ost'

    def ready(self):
        from .integracao import Notificacao
        from apscheduler.schedulers.background import BackgroundScheduler

        sheduler_ost = BackgroundScheduler(daemon=True)
        jobs = sheduler_ost.get_jobs()
        if jobs:
            sheduler_ost.shutdown()

        notificacao = Notificacao()
        sheduler_ost.configure(timezone="america/fortaleza")
        sheduler_ost.add_job(
            notificacao.shedule_api,
            'interval',
            minutes=16
        )
        sheduler_ost.add_job(
            notificacao.verificar_agenda_os,
            'interval',
            minutes=18
        )

        sheduler_ost.start()
