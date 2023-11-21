from django.db import models

# Create your models here.
class Spc(models.Model):
    solicitante = models.CharField(max_length=128)
    cod_cliente = models.IntegerField()
    data_vencimento = models.DateField()
    data_compra = models.DateField()
    valor_do_debito = models.FloatField()
    faturas_vencidas = models.IntegerField()
    tipo_de_pessoa = models.CharField(max_length=128)
    documento = models.CharField(max_length=18)
    nome_consumidor = models.CharField(max_length=128)
    cep = models.IntegerField()
    logradouro = models.CharField(max_length=128)
    numero = models.CharField(max_length=128)
    complemento = models.CharField(max_length=128)
    bairro = models.CharField(max_length=128)
    ddd = models.IntegerField()
    celular = models.IntegerField()
    email = models.EmailField()
    data_nascimento = models.DateField()
    status_spc = models.BooleanField(default=False)