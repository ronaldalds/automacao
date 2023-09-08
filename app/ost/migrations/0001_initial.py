# Generated by Django 4.2.5 on 2023-09-06 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Tecnicos',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('chat_id', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Tecnicos',
            },
        ),
        migrations.CreateModel(
            name='TempoSLA',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sla', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'SLA',
            },
        ),
        migrations.CreateModel(
            name='TiposOS',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Tipo_OS',
            },
        ),
        migrations.CreateModel(
            name='TecnicosMensagem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mensagem', models.TextField()),
                ('sla', models.IntegerField(default=0)),
                ('cod_os', models.IntegerField(default=0)),
                ('data_envio', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost.tecnicos')),
            ],
            options={
                'verbose_name_plural': 'Mensagem',
            },
        ),
        migrations.CreateModel(
            name='SLA_OS',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sla', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('id_tipo_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost.tiposos')),
            ],
            options={
                'verbose_name_plural': 'SLA_OS',
            },
        ),
        migrations.CreateModel(
            name='InformacoesOS',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=300)),
                ('id_tipo_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ost.tiposos')),
            ],
            options={
                'verbose_name_plural': 'Informacoes_OS',
            },
        ),
    ]
