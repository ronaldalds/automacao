from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from ..models import *

@admin.register(Empresa)
class EmpresaAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'razao_social',
        'nome_fantasia',
        'nome',
        'cnpj',
        'logradouro',
        'numero',
        'bairro',
        'cidade'
    )
    list_display_links = list_display
    search_fields = ['nome', 'razao_social']
