# Generated by Django 5.0.7 on 2024-10-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_product_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='vin_code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='VIN code'),
        ),
    ]
