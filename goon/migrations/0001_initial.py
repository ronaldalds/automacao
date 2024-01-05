# Generated by Django 5.0 on 2023-12-28 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusGoon',
            fields=[
                ('nome', models.CharField(max_length=64)),
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenGoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('auth', models.CharField(max_length=128)),
                ('cliente', models.CharField(max_length=128)),
            ],
        ),
    ]
