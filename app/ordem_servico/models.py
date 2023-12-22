from django.db import models


# Create your models here.
class OrdemServico(models.Model):
    mk = models.IntegerField()
    cod_pessoa = models.IntegerField()
    qtd_conexoes = models.IntegerField()
    conexao_associada = models.IntegerField()
    os_cancelamento_ou_recolhimento = models.CharField(max_length=1)
    documento = models.CharField(max_length=18)
    tipo_os = models.CharField(max_length=128)
    grupo_atendimento_os = models.CharField(max_length=128)
    detalhes_os = models.CharField(max_length=512)
    nivel_sla = models.CharField(max_length=128)
    status = models.BooleanField(default=False)
    processamento = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.documento

    class Meta:
        verbose_name_plural = 'Ordens de Serviço'


class LimiteOS(models.Model):
    mk = models.IntegerField()
    grupo_atendimento_os = models.CharField(max_length=128)
    limite = models.IntegerField()


class ThreadOs(models.Model):
    numero_thread = models.IntegerField()
