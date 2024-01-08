# Generated by Django 5.0 on 2024-01-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ost', '0003_tipoos_sla_tipoos_status_delete_slaos'),
    ]

    operations = [
        migrations.AddField(
            model_name='tecnicomensagem',
            name='nome_tecnico',
            field=models.CharField(default='asdf', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='informacaoos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tecnicomensagem',
            name='cod_os',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tecnicomensagem',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tecnicomensagem',
            name='sla',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='temposla',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]