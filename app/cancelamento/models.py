from django.db import models


class Cancelamento(models.Model):
    mk = models.IntegerField()
    contrato = models.IntegerField()
    cod_pessoa = models.IntegerField()
    tipo_os = models.CharField(max_length=128)
    defeito = models.CharField(max_length=128)
    profile = models.CharField(max_length=128)
    planos_de_contas = models.CharField(max_length=128)
    relato_do_problema = models.TextField()
    detalhes_cancelamento = models.TextField()
    grupo_atendimento_os = models.CharField(max_length=128)
    incidencia_de_multa = models.CharField(max_length=128)
    data_vcto_multa_contratual = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    motivo_cancelamento = models.CharField(max_length=128)
    valor_multa = valor_multa = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.BooleanField(default=False)
    processamento = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.contrato}"


class ThreadCancelamento(models.Model):
    numero_thread = models.IntegerField()
