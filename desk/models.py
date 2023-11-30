from django.db import models


# Create your models here.
class UserDesk(models.Model):
    nome = models.CharField(max_length=128)
    chave = models.CharField(max_length=128)


class EndPoint(models.Model):
    grupo = models.CharField(max_length=128)
    acao = models.CharField(max_length=128)
    url = models.URLField()


class Relatorio(models.Model):
    nome = models.CharField(max_length=128)
    id_relatorio = models.IntegerField()
