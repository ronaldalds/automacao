from django.db import models
from .endereco_models import Cidade


class Empresa(models.Model):
    razao_social = models.CharField(max_length=128)
    nome_fantasia = models.CharField(max_length=128)
    nome = models.CharField(max_length=128)
    cnpj = models.CharField(max_length=128)
    logradouro = models.CharField(max_length=128)
    numero = models.CharField(max_length=128)
    bairro = models.CharField(max_length=128)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Empresas"

    def __str__(self) -> str:
        return self.nome_fantasia
