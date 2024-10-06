# Generated by Django 5.0.7 on 2024-10-06 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branches', '0002_alter_branch_options'),
        ('inventory', '0002_initial'),
        ('users', '0003_alter_supplier_debt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchFundTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Daily fund amount')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='branches.branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Branch Fund',
                'verbose_name_plural': 'Branch Funds',
            },
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt_amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debt amount')),
                ('is_debt', models.BooleanField(default=False, verbose_name='Is debt')),
                ('current_debt', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Current debt')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_supplier', to='users.supplier', verbose_name='Supplier')),
            ],
            options={
                'verbose_name': 'Debt',
                'verbose_name_plural': 'Debts',
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
            ],
            options={
                'verbose_name': 'Expense Type',
                'verbose_name_plural': 'Expense Types',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
                ('from_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.expensetype', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
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
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.supplier', verbose_name='Supplier')),
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
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Debt')),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Buy price')),
                ('total_summ', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Total summ')),
                ('import_list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.importlist', verbose_name='Import list')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Import product',
                'verbose_name_plural': 'Import products',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches.branch', verbose_name='Branch')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_employee', to='users.employee', verbose_name='Employee')),
                ('from_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
            },
        ),
    ]
