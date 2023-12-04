from django.contrib import admin
from .models import OrdemServico


# Register your models here.
@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'mk',
                    'contrato',
                    'conexao_associada',
                    'documento',
                    'grupo_atendimento_os',
                    'status_recolhimento',
                    )
    list_filter = ('status_recolhimento', 'mk',)
    search_fields = ['contrato', 'conexao_associada', 'grupo_atendimento_os',]
