from django.db import models


# Create your models here.
class TokenGoon(models.Model):
    nome = models.CharField(max_length=128)
    auth = models.CharField(max_length=128)
    cliente = models.CharField(max_length=128)


class StatusGoon(models.Model):
    nome = models.CharField(max_length=64)
    descricao = models.CharField(max_length=128)


class UrlGoon(models.Model):
    url = models.URLField()
