from django.db import models


# Create your models here.
class Alerta(models.Model):
    nome = models.CharField(max_length=128)
    velocidade = models.IntegerField()
    tipo = models.IntegerField()
    ciclo = models.IntegerField()


class Api(models.Model):
    key = models.CharField(max_length=128)
    secret = models.CharField(max_length=128)
