# Generated by Django 5.0.7 on 2024-10-12 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_orderservice_part_alter_orderproduct_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='manager_share',
        ),
    ]
