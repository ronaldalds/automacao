from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "automovel",
                    "placa",
                    "velocidade",
                    "horario",
                    "enviado",
                    )
    list_filter = ("placa",
                   "enviado",
                   )
    search_fields = ["automovel", "placa", "horario",]