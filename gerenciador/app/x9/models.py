from django.db import models

# Create your models here.
class Alerta(models.Model):
    automovel = models.CharField(max_length=128)
    placa = models.CharField(max_length=7)
    velocidade = models.IntegerField()
    horario = models.DateTimeField()
    enviado = models.BooleanField(default=False)
