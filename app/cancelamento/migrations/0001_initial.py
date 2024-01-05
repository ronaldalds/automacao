# Generated by Django 5.0 on 2024-01-03 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cancelamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mk', models.IntegerField()),
                ('contrato', models.IntegerField()),
                ('cod_pessoa', models.IntegerField()),
                ('tipo_os', models.CharField(max_length=128)),
                ('defeito', models.CharField(max_length=128)),
                ('profile', models.CharField(max_length=128)),
                ('planos_de_contas', models.CharField(max_length=128)),
                ('relato_do_problema', models.TextField()),
                ('detalhes_cancelamento', models.TextField()),
                ('grupo_atendimento_os', models.CharField(max_length=128)),
                ('incidencia_de_multa', models.CharField(max_length=128)),
                ('data_vcto_multa_contratual', models.CharField(blank=True, max_length=128, null=True)),
                ('motivo_cancelamento', models.CharField(max_length=128)),
                ('valor_multa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=False)),
                ('processamento', models.BooleanField(default=False)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadCancelamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_thread', models.IntegerField()),
            ],
        ),
    ]
