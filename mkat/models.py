from django.db import models


# Create your models here.
class UserMkat(models.Model):
    nome = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
