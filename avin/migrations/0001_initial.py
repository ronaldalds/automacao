# Generated by Django 5.0 on 2024-01-03 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TokenAvin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('auth', models.CharField(max_length=128)),
                ('cliente', models.CharField(max_length=128)),
            ],
        ),
    ]
