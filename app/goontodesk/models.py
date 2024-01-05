from django.db import models


class OsGoon(models.Model):
    numero_os = models.IntegerField(primary_key=True, unique=True)
    ordem_servico_externa = models.CharField(
        max_length=11,
        null=True,
        blank=True
    )
    descricao = models.CharField(max_length=256)
    tipo_servico = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.numero_os}"


class StatusInfo(models.Model):
    sequencia = models.IntegerField()
    status = models.CharField(max_length=8)
    data = models.CharField(max_length=64)
    mobile_agent = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    mobile_phone = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    os_goon = models.ForeignKey(
        OsGoon,
        on_delete=models.CASCADE,
        related_name="status_info"
    )
    enviado = models.BooleanField(default=False)
