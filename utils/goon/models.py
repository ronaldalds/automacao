from django.db import models


class TokenGoon(models.Model):
    nome = models.CharField(max_length=128)
    auth = models.CharField(max_length=128)
    cliente = models.CharField(max_length=128)


class StatusGoon(models.Model):
    nome = models.CharField(max_length=64)
    descricao = models.CharField(max_length=128, primary_key=True, unique=True)
