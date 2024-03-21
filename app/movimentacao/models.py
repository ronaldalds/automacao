from django.db import models


class Movimentacao(models.Model):
    id = models.IntegerField(primary_key=True)
    mk = models.IntegerField()
    status = models.BooleanField(default=False)
    processamento = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ThreadMovimentacao(models.Model):
    numero_thread = models.IntegerField()
