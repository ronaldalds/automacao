from django.db import models


# Create your models here.
class Cancelamento(models.Model):
    mk = models.IntegerField()
    contrato = models.IntegerField()
    cod_pessoa = models.IntegerField()
    conexao = models.IntegerField()
    os_cancelamento_30d = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    documento_codigo = models.CharField(max_length=128)
    tipo_os = models.CharField(max_length=128)
    planos_de_contas = models.CharField(max_length=128)
    relato_do_problema = models.TextField()
    detalhes_cancelamento = models.TextField()
    grupo_atendimento_os = models.CharField(max_length=128)
    incidencia_de_multa = models.CharField(max_length=128)
    valor_multa = valor_multa = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    data_vcto_multa_contratual = models.CharField(max_length=128)
    data_a_cancelar = models.CharField(max_length=128)
    loja = models.CharField(max_length=128)
    onu_serial = models.CharField(max_length=128)
    status = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.documento_codigo
