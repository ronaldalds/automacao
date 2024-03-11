import re
from django.db import models
from django.core.exceptions import ValidationError


class Chamado(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=11,
        help_text="ex: 0923-000052"
    )
    data_criacao = models.DateField()
    andamento = models.BooleanField(default=True)
    data_finalizacao = models.DateField(null=True, blank=True)
    assunto = models.CharField(max_length=256)
    nome_categoria = models.CharField(max_length=256)
    total_horas_1_2_atendimento_str = models.CharField(
        max_length=32,
        help_text="ex: 0000:04:00"
    )
    total_horas_1_2_atendimento = models.FloatField(
        editable=False
    )
    nome_sla_status_atual = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    sla_2_expirado = models.CharField(max_length=128)
    first_call = models.CharField(max_length=1, help_text="ex: N ou S")
    nome_operador = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    nome_status = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    sla_1_expirado = models.CharField(max_length=128, null=True, blank=True)
    total_horas_1_atendimento_str = models.CharField(
        max_length=32,
        help_text="ex: 0000:04:00",
    )
    total_horas_1_atendimento = models.FloatField(
        editable=False,
    )

    def clean(self):
        id_pattern = r"^(0[1-9]|1[0-2])(\d{2})-\d{6}$"
        total_horas_1_2_atendimento_pattern = re.compile(
            r'^\d+:\d{1,2}:\d{2}$'
        )

        if not re.match(id_pattern, self.id):
            raise ValidationError(
                "O chamado deve estar no formato '0923-000052'."
            )
        if not re.match(
            total_horas_1_2_atendimento_pattern,
            self.total_horas_1_2_atendimento_str
        ):
            raise ValidationError(
                "A total horas deve estar no formato 'HH:MM:SS'."
            )
        if not re.match(
            total_horas_1_2_atendimento_pattern,
            self.total_horas_1_atendimento_str
        ):
            raise ValidationError(
                "A total horas deve estar no formato 'HH:MM:SS'."
            )

    def save(self, *args, **kwargs):
        if self.total_horas_1_2_atendimento_str != "0":
            horas_1_2, minutos_1_2, segundos_1_2 = map(
                int,
                self.total_horas_1_2_atendimento_str.split(':')
            )
            total_1_2 = horas_1_2 + minutos_1_2 / 60 + segundos_1_2 / 3600
            self.total_horas_1_2_atendimento = total_1_2
        else:
            self.total_horas_1_2_atendimento_str = "00:00:00"
            self.total_horas_1_2_atendimento = 0.0

        if self.total_horas_1_atendimento_str:
            horas_1, minutos_1, segundos_1 = map(
                int,
                self.total_horas_1_atendimento_str.split(':')
            )
            total_1 = horas_1 + minutos_1 / 60 + segundos_1 / 3600
            self.total_horas_1_atendimento = total_1
        else:
            self.total_horas_1_atendimento = 0.0

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Chamados'

    def __str__(self):
        return self.id


class Interacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.PROTECT)
    status_acao_nome_relatorio = models.CharField(max_length=128)
    fantasia_fornecedor = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    seguencia = models.IntegerField()
    chamado_aprovadores = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    tempo_corrido_interacao_str = models.CharField(
        max_length=32,
        help_text="ex: 0000:04:00",
        null=True,
        blank=True
    )
    tempo_corrido_interacao = models.FloatField(
        editable=False,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.chamado_aprovadores:
            self.chamado_aprovadores = self.chamado_aprovadores.split(":")[0]
        if self.tempo_corrido_interacao_str:
            horas, minutos, segundos = map(
                int,
                self.tempo_corrido_interacao_str.split(':')
            )
            total = horas + minutos / 60 + segundos / 3600
            self.tempo_corrido_interacao = total

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Interações'

    def __str__(self):
        return f"{self.chamado} - {self.seguencia}"
