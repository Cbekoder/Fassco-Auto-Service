# Generated by Django 5.0.7 on 2024-10-06 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0004_alter_wallet_name'),
        ('transactions', '0002_alter_importproduct_amount'),
        ('users', '0005_client_lending'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lending_amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Lending amount')),
                ('is_lending', models.BooleanField(default=False, verbose_name='Is lending')),
                ('current_lending', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Current lending')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_client', to='users.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Lending',
                'verbose_name_plural': 'Lendings',
            },
        ),
    ]
