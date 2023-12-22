from django.db import models


class Tecnico(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    chat_id = models.IntegerField(null=False)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tecnicos'

    def __str__(self) -> str:
        return self.nome


class TipoOs(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=300, null=False)

    def __str__(self) -> str:
        return str(self.tipo)

    class Meta:
        verbose_name_plural = 'Tipo O.S.'


class TecnicoMensagem(models.Model):
    id = models.BigAutoField(primary_key=True)
    chat_id = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    mensagem = models.TextField()
    sla = models.IntegerField(null=False, default=0)
    cod_os = models.IntegerField(null=False, default=0)
    data_envio = models.DateTimeField(auto_now=True)
    status = models.BooleanField(null=False, default=True)

    def __str__(self) -> str:
        return str(self.chat_id)

    class Meta:
        verbose_name_plural = 'Mensagens'


class TempoSla(models.Model):
    id = models.BigAutoField(primary_key=True)
    sla = models.IntegerField(null=False)

    def __str__(self) -> str:
        return str(self.sla)

    class Meta:
        verbose_name_plural = 'S.L.A.'


class SlaOs(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_os = models.ForeignKey(TipoOs, on_delete=models.CASCADE)
    sla = models.IntegerField(null=False)
    status = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name_plural = 'S.L.A. O.S.'


class InformacaoOs(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_os = models.ForeignKey(TipoOs, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300, null=False)

    def __str__(self) -> str:
        return f"{self.nome} - {self.id_tipo_os}"

    class Meta:
        verbose_name_plural = 'Informacões O.S.'


class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_envio = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Logs'
