# Generated by Django 5.0.7 on 2024-10-11 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0002_alter_wallet_options_alter_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Balance'),
        ),
    ]
