from django.contrib.admin import register
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from ..models import (
    Operacao,
    Estado,
    Cidade
)


@register(Operacao)
class OperacaoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome')
    list_display_links = list_display
    search_fields = ['nome']


@register(Estado)
class EstadoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome', 'operacao', 'uf')
    list_display_links = list_display
    list_filter = ('operacao',)
    search_fields = ['nome']


@register(Cidade)
class CidadeAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'municipio',
        'localidade',
        'sigla_municipio',
        'sigla_localidade',
        'cod_cidade',
        'estado',
    )
    list_display_links = list_display
    list_filter = ('estado',)
    search_fields = ['municipio', 'localidade']
    readonly_fields = ['cod_cidade',]
