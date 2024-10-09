# Generated by Django 5.0.7 on 2024-10-07 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt_amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debt amount')),
                ('is_debt', models.BooleanField(default=False, verbose_name='Is debt')),
                ('current_debt', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Current debt')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Debt',
                'verbose_name_plural': 'Debts',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Expense Type',
                'verbose_name_plural': 'Expense Types',
            },
        ),
        migrations.CreateModel(
            name='ImportList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Total')),
                ('paid', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Paid')),
                ('debt', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debt')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Import list',
                'verbose_name_plural': 'Import lists',
            },
        ),
        migrations.CreateModel(
            name='ImportProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=1, verbose_name='Debt')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Buy price')),
                ('total_summ', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Total summ')),
            ],
            options={
                'verbose_name': 'Import product',
                'verbose_name_plural': 'Import products',
            },
        ),
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lending_amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Lending amount')),
                ('is_lending', models.BooleanField(default=False, verbose_name='Is lending')),
                ('current_lending', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Current lending')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Lending',
                'verbose_name_plural': 'Lendings',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
            },
        ),
        migrations.CreateModel(
            name='BranchFundTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Daily fund amount')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='branches.branch')),
            ],
            options={
                'verbose_name': 'Branch Fund',
                'verbose_name_plural': 'Branch Funds',
            },
        ),
    ]
