from django.db import models


class UserMkat(models.Model):
    nome = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
