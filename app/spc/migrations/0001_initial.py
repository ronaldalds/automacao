# Generated by Django 5.0.1 on 2024-01-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitante', models.CharField(max_length=128)),
                ('cod_cliente', models.IntegerField()),
                ('data_vencimento', models.DateField()),
                ('data_compra', models.DateField()),
                ('valor_do_debito', models.FloatField()),
                ('faturas_vencidas', models.IntegerField()),
                ('tipo_de_pessoa', models.CharField(max_length=128)),
                ('documento', models.CharField(max_length=18)),
                ('nome_consumidor', models.CharField(max_length=128)),
                ('cep', models.IntegerField()),
                ('logradouro', models.CharField(max_length=128)),
                ('numero', models.CharField(max_length=128)),
                ('complemento', models.CharField(max_length=128)),
                ('bairro', models.CharField(max_length=128)),
                ('ddd', models.IntegerField()),
                ('celular', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('data_nascimento', models.DateField()),
                ('status_spc', models.BooleanField(default=False)),
            ],
        ),
    ]
