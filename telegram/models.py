from django.db import models


class UserTelegram(models.Model):
    FUNCAO = [
        (1, "Técnico"),
        (2, "Outros")
    ]
    id = models.IntegerField(primary_key=True, unique=True)
    nome = models.CharField(max_length=128)
    funcao = models.IntegerField(choices=FUNCAO, default=2)
    status = models.BooleanField(default=True)


class ApiTelegram(models.Model):
    id = models.IntegerField(primary_key=True)
    hash = models.CharField(max_length=128)


class BotTelegram(models.Model):
    nome = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
