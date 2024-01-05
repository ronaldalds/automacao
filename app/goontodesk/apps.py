from django.apps import AppConfig


class GoontodeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.goontodesk'

    def ready(self):
        from .integracao import GoonToDesk
        from apscheduler.schedulers.background import BackgroundScheduler

        interacao = GoonToDesk()
        scheduler = BackgroundScheduler(daemon=True)
        jobs = scheduler.get_jobs()
        if jobs:
            scheduler.shutdown()
        scheduler.add_job(interacao.get_os_goon, 'interval', minutes=10)
        scheduler.start()
