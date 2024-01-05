# Generated by Django 5.0 on 2024-01-04 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorOs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(max_length=32)),
                ('tipo', models.CharField(max_length=32)),
                ('operador', models.CharField(max_length=32)),
                ('detalhe', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data_envio', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='TecnicoMensagem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('chat_id', models.IntegerField()),
                ('mensagem', models.TextField()),
                ('sla', models.IntegerField(default=0)),
                ('cod_os', models.IntegerField(default=0)),
                ('data_envio', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Mensagens',
            },
        ),
        migrations.CreateModel(
            name='TempoSla',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sla', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'S.L.A.',
            },
        ),
        migrations.CreateModel(
            name='TipoOs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Tipo O.S.',
            },
        ),
        migrations.CreateModel(
            name='SlaOs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sla', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('id_tipo_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost.tipoos')),
            ],
            options={
                'verbose_name_plural': 'S.L.A. O.S.',
            },
        ),
        migrations.CreateModel(
            name='InformacaoOs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=300)),
                ('id_tipo_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost.tipoos')),
            ],
            options={
                'verbose_name_plural': 'Informacões O.S.',
            },
        ),
    ]
