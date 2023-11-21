from django.db import models


class Tecnico(models.Model):
    nome = models.CharField(max_length=200)
    login_mk = models.CharField(max_length=200)
    chat_id = models.IntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tecnicos"

    def __str__(self) -> str:
        return self.nome

class TipoOS(models.Model):
    tipo = models.CharField(max_length=200)
    sla = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Tipo_OS"

class Mensagem(models.Model):
    tecnico_id = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    alerta_id = models.ForeignKey("AlertaSLA", on_delete=models.SET_NULL, null=True)
    mensagem = models.TextField()
    cod_os = models.IntegerField(default=0)
    data_envio = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Mensagens"

class AlertaSLA(models.Model):
    hora = models.IntegerField()

    def __str__(self) -> str:
        return self.hora

    class Meta:
        verbose_name_plural = "Alertas"

class InformacaoOS(models.Model):
    id_tipo_os = models.ForeignKey(TipoOS, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        verbose_name_plural = "Informacoes_OS"
