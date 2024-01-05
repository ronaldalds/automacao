from django.db import models


class TipoOs(models.Model):
    tipo = models.CharField(max_length=300)
    sla = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.tipo)

    class Meta:
        verbose_name_plural = 'Tipo O.S.'


class TecnicoMensagem(models.Model):
    nome_tecnico = models.CharField(max_length=128)
    chat_id = models.IntegerField()
    mensagem = models.TextField()
    sla = models.IntegerField()
    cod_os = models.IntegerField()
    data_envio = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.chat_id)

    class Meta:
        verbose_name_plural = 'Mensagens'


class TempoSla(models.Model):
    sla = models.IntegerField(primary_key=True, unique=True)

    def __str__(self) -> str:
        return f"{self.sla}"

    class Meta:
        verbose_name_plural = 'S.L.A.'


class InformacaoOs(models.Model):
    id_tipo_os = models.ForeignKey(TipoOs, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.nome} - {self.id_tipo_os}"

    class Meta:
        verbose_name_plural = 'Informacões O.S.'


class Log(models.Model):
    data_envio = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Logs'


class ErrorOs(models.Model):
    os = models.CharField(max_length=32)
    tipo = models.CharField(max_length=32)
    operador = models.CharField(max_length=32)
    detalhe = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now=True)
