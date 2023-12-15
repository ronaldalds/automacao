from django.apps import AppConfig


# Importe o modelo Ativado do seu aplicativo
class OstConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.ost'

    def ready(self):
        from .utils import Notificacao
        from apscheduler.schedulers.background import BackgroundScheduler
        sheduler = BackgroundScheduler(daemon=True)
        notificacao = Notificacao()
        sheduler.configure(timezone="america/fortaleza")
        sheduler.add_job(notificacao.shedule_api, 'interval', minutes=10)
        sheduler.add_job(notificacao.verificar_agenda_os, 'interval', minutes=15)

        sheduler.start()
