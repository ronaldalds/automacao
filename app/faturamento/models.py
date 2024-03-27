from django.db import models


class FaturamentoLog(models.Model):
    mk = models.IntegerField()
    data_faturamento = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
