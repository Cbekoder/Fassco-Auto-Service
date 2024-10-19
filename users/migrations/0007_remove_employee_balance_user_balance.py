# Generated by Django 5.0.7 on 2024-10-19 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_client_options_alter_employee_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='balance',
        ),
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
