from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'login_mk','chat_id', 'status')
    list_filter = ('status',)
    search_fields = ['nome',]

@admin.register(TipoOS)
class TipoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'sla')
    list_filter = ('sla',)
    search_fields = ['tipo',]

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'tecnico_id', 'alerta_id', 'mensagem','cod_os', 'data_envio', 'status')
    list_filter = ('tecnico_id', 'status')
    search_fields = ['tecnico_id',]

@admin.register(AlertaSLA)
class AlertaSLAAdmin(admin.ModelAdmin):
    list_display = ('id', 'hora')
    search_fields = ['hora',]

@admin.register(InformacaoOS)
class InformacaoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_tipo_os', 'nome')
    list_filter = ('id_tipo_os',)