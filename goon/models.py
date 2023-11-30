from django.db import models


# Create your models here.
class Api(models.Model):
    nome = models.CharField(max_length=128)
    auth = models.CharField(max_length=128)
    cliente_code = models.CharField(max_length=128)
