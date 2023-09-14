from django.db import models

# Create your models here.
class Cancelamento(models.Model):
    mk = models.IntegerField()
    contrato = models.IntegerField()
    atraso = models.IntegerField()
    cod_pessoa = models.IntegerField()
    conexao = models.IntegerField()
    documento = models.CharField(max_length=18)
    tipo_os = models.CharField(max_length=128)
    planos_de_contas = models.CharField(max_length=128)
    relato_do_problema = models.CharField(max_length=512)
    detalhes_cancelamento = models.CharField(max_length=512)
    grupo_atendimento_os = models.CharField(max_length=128)
    incidencia_de_multa = models.BooleanField(default=False)
    valor_multa = models.FloatField()
    data_vcto_multa_contratual = models.DateField()
    data_a_cancelar = models.DateField()
    loja = models.CharField(max_length=128)
    onu_serial = models.CharField(max_length=128)
    status_cancelamento = models.BooleanField(default=False)