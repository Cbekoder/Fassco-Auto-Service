# Generated by Django 5.0.7 on 2024-10-09 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_employee_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('manager', 'Manager'), ('mechanic', 'Mechanic'), ('other', 'Other')], max_length=15),
        ),
    ]
