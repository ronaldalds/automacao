from django.db import models


class TokenDesk(models.Model):
    nome = models.CharField(max_length=128)
    operador = models.CharField(max_length=128)
    ambiente = models.CharField(max_length=128)


class StatusDesk(models.Model):
    nome = models.CharField(max_length=128)
    id = models.CharField(max_length=128, primary_key=True, unique=True)


class FormaAtendimentoDesk(models.Model):
    nome = models.CharField(max_length=128)
    id = models.CharField(max_length=128, primary_key=True, unique=True)
