from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "automovel",
        "placa",
        "velocidade",
        "horario",
        "enviado",
    )
    list_display_links = list_display
    list_filter = ("placa", "enviado")
    search_fields = ["automovel", "placa", "horario"]
