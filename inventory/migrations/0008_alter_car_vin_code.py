# Generated by Django 5.0.7 on 2024-10-23 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_product_arrival_price_alter_product_sell_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='vin_code',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='VIN code'),
        ),
    ]
