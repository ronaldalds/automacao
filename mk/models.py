from django.db import models


# Create your models here.
class Login(models.Model):
    mk = models.IntegerField()
    url = models.URLField()
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)


class TipoOS(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class Profile(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class NivelSLA(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class MotivoCancelamento(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class GrupoAtendimento(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class Defeito(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)


class Faturamento(models.Model):
    id_web = models.IntegerField()
    mk = models.IntegerField()
    descricao = models.CharField(max_length=128)
