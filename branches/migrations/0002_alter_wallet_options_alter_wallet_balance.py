# Generated by Django 5.0.7 on 2024-10-09 02:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'verbose_name': 'Wallet', 'verbose_name_plural': 'Wallet'},
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
