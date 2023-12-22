from django.db import models


class TokenDesk(models.Model):
    nome = models.CharField(max_length=128)
    operador = models.CharField(max_length=128)
    ambiente = models.CharField(max_length=128)


class EndPointDesk(models.Model):
    grupo = models.CharField(max_length=128)
    acao = models.CharField(max_length=128)
    url = models.URLField()


class StatusDesk(models.Model):
    nome = models.CharField(max_length=128)
    descricao = models.CharField(max_length=128)


class FormaAtendimentoDesk(models.Model):
    nome = models.CharField(max_length=128)
    descricao = models.CharField(max_length=128)
