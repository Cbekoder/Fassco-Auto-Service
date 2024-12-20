# Generated by Django 5.0.7 on 2024-10-24 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_orderproduct_discount_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=15, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='orderservice',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=15, verbose_name='Discount'),
        ),
    ]
