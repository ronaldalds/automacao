from django.contrib.admin import ModelAdmin, register
from .models import Alerta


@register(Alerta)
class AlertaAdmin(ModelAdmin):
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
