from django.db import models


class Tecnicos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    chat_id = models.IntegerField(null=False)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tecnicos"

    def __str__(self) -> str:
        return self.nome

class TiposOS(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=300, null=False)

    class Meta:
        verbose_name_plural = "Tipo_OS"

class TecnicosMensagem(models.Model):
    id = models.BigAutoField(primary_key=True)
    chat_id = models.ForeignKey(Tecnicos, on_delete=models.CASCADE)
    mensagem = models.TextField()
    sla = models.IntegerField(null=False, default=0)
    cod_os = models.IntegerField(null=False, default=0)
    data_envio = models.DateTimeField(auto_now=True)
    status = models.BooleanField(null=False, default=True)

    def __str__(self) -> str:
        return str(self.chat_id)

    class Meta:
        verbose_name_plural = "Mensagem"

class TempoSLA(models.Model):
    id = models.BigAutoField(primary_key=True)
    sla = models.IntegerField(null=False)

    def __str__(self) -> str:
        return str(self.sla)

    class Meta:
        verbose_name_plural = "SLA"

class SLA_OS(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_os = models.ForeignKey(TiposOS, on_delete=models.CASCADE)
    sla = models.IntegerField(null=False)
    status = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name_plural = "SLA_OS"

class InformacoesOS(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_os = models.ForeignKey(TiposOS, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300, null=False)

    class Meta:
        verbose_name_plural = "Informacoes_OS"

class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_envio = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Logs"