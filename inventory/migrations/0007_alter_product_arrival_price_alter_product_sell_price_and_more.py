# Generated by Django 5.0.7 on 2024-10-23 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_car_vin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='arrival_price',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Import price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sell_price',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Export price'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Price'),
        ),
    ]
