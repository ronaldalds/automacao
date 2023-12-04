from django.db import models


# Create your models here.
class OrdemServico(models.Model):
    solicitante = models.CharField(max_length=128)
    mk = models.IntegerField()
    contrato = models.IntegerField()
    qtd_conexoes = models.IntegerField()
    conexao_associada = models.IntegerField()
    qtd_atendimentos = models.IntegerField()
    os_cancelamento_ou_recolhimento = models.BooleanField(default=False)
    documento = models.CharField(max_length=18)
    tipo_os = models.CharField(max_length=128)
    planos_de_contas = models.CharField(max_length=128)
    grupo_atendimento_os = models.CharField(max_length=128)
    detalhes_os = models.CharField(max_length=512)
    atraso_max = models.IntegerField()
    loja = models.CharField(max_length=128)
    status_recolhimento = models.BooleanField(default=False)


class LimiteOS(models.Model):
    mk = models.IntegerField()
    loja = models.CharField(max_length=128)
    limite = models.IntegerField()
