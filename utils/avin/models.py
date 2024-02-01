from django.db import models


class TokenAvin(models.Model):
    nome = models.CharField(max_length=128)
    auth = models.CharField(max_length=128)
    cliente = models.CharField(max_length=128)
