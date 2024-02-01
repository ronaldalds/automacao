from django.db import models


class Operacao(models.Model):
    nome = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Operações"

    def __str__(self) -> str:
        return self.nome


class Estado(models.Model):
    nome = models.CharField(max_length=128)
    uf = models.CharField(max_length=2)
    operacao = models.ForeignKey(Operacao, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Estados"

    def __str__(self) -> str:
        return self.uf


class Cidade(models.Model):
    municipio = models.CharField(max_length=128)
    sigla_municipio = models.CharField(max_length=3)
    localidade = models.CharField(max_length=128, null=True, blank=True)
    sigla_localidade = models.CharField(max_length=3, null=True, blank=True)
    cod_cidade = models.CharField(max_length=7)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Cidades"

    def save(self, *args, **kwargs):
        if self.localidade:
            self.cod_cidade = f"{self.sigla_municipio}-{self.sigla_localidade}"
        else:
            self.cod_cidade = self.sigla_municipio
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.localidade:
            return f"{self.municipio}/{self.localidade} - {self.estado.uf}"

        return f"{self.municipio} - {self.estado.uf}"
