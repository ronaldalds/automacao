# Generated by Django 5.0.1 on 2024-03-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='mk',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
