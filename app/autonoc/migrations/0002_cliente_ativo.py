# Generated by Django 5.0.1 on 2024-02-06 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autonoc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
