from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'chat_id', 'status')
    list_filter = ('status',)
    search_fields = ['nome',]

@admin.register(TipoOS)
class TipoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ['tipo',]

@admin.register(TecnicoMensagem)
class TecnicoMensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'sla', 'cod_os', 'data_envio', 'status')
    list_filter = ('chat_id',)
    search_fields = ['chat_id',]

@admin.register(TempoSLA)
class TempoSLAAdmin(admin.ModelAdmin):
    list_display = ('id', 'sla')
    search_fields = ['sla',]

@admin.register(SlaOS)
class SlaOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_tipo_os', 'sla', 'status')
    list_filter = ('sla', 'status',)

@admin.register(InformacaoOS)
class InformacaoOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_tipo_os', 'nome')
    list_filter = ('id_tipo_os',)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_envio')
    list_filter = ('data_envio',)
