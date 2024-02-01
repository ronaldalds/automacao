from django.db import models
from .conexao_models import Conexao, FormaPagamento


class Faturamento(models.Model):
    conexao = models.ForeignKey(Conexao, on_delete=models.PROTECT)
    valor = models.FloatField()
    vencimento = models.DateField()
    valor_faturado = models.FloatField()
    valor_recebido = models.FloatField()
    saldo = models.FloatField()
    data_pagamento = models.DateField()
    nf = models.IntegerField()
    data_nf = models.DateField()
    data_envio_nf = models.DateField()

    class Meta:
        verbose_name_plural = "Faturamentos"

    def __str__(self) -> str:
        return f"{self.conexao} - {self.vencimento}"


class FinanceiroCliente(models.Model):
    conexao = models.ForeignKey(Conexao, on_delete=models.PROTECT)
    forma_de_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT
    )
    saldo_a_pagar = models.FloatField()
    data_debito = models.DateField()
