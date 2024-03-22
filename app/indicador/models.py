import re
from django.db import models
from django.core.exceptions import ValidationError


class Chamado(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=11,
        help_text="ex: 0923-000052"
    )
    nome_categoria = models.CharField(max_length=256)
    assunto = models.CharField(max_length=256)
    data_criacao = models.DateField()
    andamento = models.BooleanField(default=True)
    data_finalizacao = models.DateField(null=True, blank=True)
    nome_operador = models.CharField(max_length=128, null=True, blank=True)
    sla_1_expirado = models.CharField(max_length=128, null=True, blank=True)
    total_horas_1_atendimento = models.FloatField(editable=False, null=True, blank=True)
    nome_status = models.CharField(max_length=128, null=True, blank=True)
    first_call = models.CharField(max_length=1, help_text="ex: N ou S")
    sla_2_expirado = models.CharField(max_length=128)
    total_horas_1_2_atendimento = models.FloatField(editable=False, null=True, blank=True)
    nome_sistema = models.CharField(max_length=128, null=True, blank=True)
    tempo_restante_1 = models.FloatField(editable=False, null=True, blank=True)
    tempo_restante_2 = models.FloatField(editable=False, null=True, blank=True)
    nome_grupo = models.CharField(max_length=256, null=True, blank=True)
    nome_sla_status_atual = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    def clean(self):
        id_pattern = r"^(0[1-9]|1[0-2])(\d{2})-\d{6}$"
        if not re.match(id_pattern, self.id):
            raise ValidationError(
                "O chamado deve estar no formato '0923-000052'."
            )

    class Meta:
        verbose_name_plural = 'Chamados'

    def __str__(self):
        return self.id


class Interacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.PROTECT)
    seguencia = models.IntegerField()
    status_acao_nome_relatorio = models.CharField(max_length=128)
    fantasia_fornecedor = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    chamado_aprovadores = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    tempo_corrido_interacao = models.FloatField(
        editable=False,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Interações'

    def __str__(self):
        return f"{self.chamado} - {self.seguencia}"
