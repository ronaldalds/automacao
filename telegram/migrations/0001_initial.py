# Generated by Django 5.0 on 2024-01-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiTelegram',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('hash', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='BotTelegram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=128)),
                ('token', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserTelegram',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=128)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
