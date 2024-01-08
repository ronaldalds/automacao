# Generated by Django 5.0 on 2023-12-28 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormaAtendimentoDesk',
            fields=[
                ('nome', models.CharField(max_length=128)),
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusDesk',
            fields=[
                ('nome', models.CharField(max_length=128)),
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenDesk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('operador', models.CharField(max_length=128)),
                ('ambiente', models.CharField(max_length=128)),
            ],
        ),
    ]