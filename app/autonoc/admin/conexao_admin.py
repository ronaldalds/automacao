from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from ..models import *

@admin.register(StatusContrato)
class StatusContratoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome', 'observacao')
    list_display_links = list_display
    search_fields = ['nome']

@admin.register(Consultor)
class ConsultorAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome', 'telefone', 'ativo')
    list_display_links = list_display
    list_filter = ('ativo',)
    search_fields = ['nome']

@admin.register(ServicoContrato)
class ServicoContratoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome')
    list_display_links = list_display
    search_fields = ['nome']

@admin.register(CanalVenda)
class CanalVendaAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'nome')
    list_display_links = list_display
    search_fields = ['nome']

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(ImportExportMixin, VersionAdmin):
    list_display = ('id', 'tipo')
    list_display_links = list_display
    search_fields = ['tipo']

@admin.register(Conexao)
class ConexaoAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'operacao',
        'empresa',
        'cod',
        'canal_venda',
        'status',
        'cliente',
        'logradouro_instalacao',
        'cidade_instalacao',
        'servico_contrato',
        'banda_contrato',
        'data_contrato',
        'data_ativacao',
        'data_vencimento',
        'observacao',
        'consultor',
        'sinal',
        'banda_reducao',
        'designacao',
        'ativo',
    )
    list_display_links = list_display
    list_filter = ('cidade_instalacao', 'operacao', 'status', 'sinal', 'ativo')
    search_fields = ['cliente__nome_fantasia', 'cliente__cnpj']
    readonly_fields = [
        'designacao',
    ]