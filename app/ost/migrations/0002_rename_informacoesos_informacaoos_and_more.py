# Generated by Django 4.2.6 on 2023-11-29 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ost', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InformacoesOS',
            new_name='InformacaoOS',
        ),
        migrations.RenameModel(
            old_name='SLA_OS',
            new_name='SlaOS',
        ),
        migrations.RenameModel(
            old_name='Tecnicos',
            new_name='Tecnico',
        ),
        migrations.RenameModel(
            old_name='TecnicosMensagem',
            new_name='TecnicoMensagem',
        ),
        migrations.RenameModel(
            old_name='TiposOS',
            new_name='TipoOS',
        ),
    ]
