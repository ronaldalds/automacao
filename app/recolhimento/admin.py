from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Recolhimento)
class RecolhimentoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'mk',
                    'contrato',
                    'conexao_associada',
                    'documento',
                    'grupo_atendimento_os',
                    'status_recolhimento',
                    )
    list_filter = ('status_recolhimento', 'mk',)
    search_fields = ['contrato','conexao_associada', 'grupo_atendimento_os',]