# Generated by Django 5.0 on 2024-01-05 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ost', '0004_tecnicomensagem_nome_tecnico_alter_informacaoos_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temposla',
            name='id',
        ),
        migrations.AlterField(
            model_name='temposla',
            name='sla',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]