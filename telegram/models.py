from django.db import models


# Create your models here.
class UserTelegram(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=128)


class ApiTelegram(models.Model):
    id = models.IntegerField(primary_key=True)
    hash = models.CharField(max_length=128)


class Bot(models.Model):
    nome = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
