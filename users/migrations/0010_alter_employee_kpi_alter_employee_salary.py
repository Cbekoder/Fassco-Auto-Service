# Generated by Django 5.0.7 on 2024-10-19 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_usertemp_balance_employee_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='kpi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
