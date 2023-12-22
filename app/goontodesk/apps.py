from django.apps import AppConfig
from threading import Thread
from .integracao import goon_to_desk


class GoontodeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.goontodesk'

    def ready(self) -> None:
        # Criando e iniciando o thread
        thread = Thread(target=goon_to_desk)
        thread.start()
