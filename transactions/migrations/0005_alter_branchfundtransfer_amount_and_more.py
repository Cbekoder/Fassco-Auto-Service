# Generated by Django 5.0.7 on 2024-10-23 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_rename_from_user_id_salary_from_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchfundtransfer',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Daily fund amount'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='current_debt',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Current debt'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='debt_amount',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Debt amount'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='importlist',
            name='debt',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Debt'),
        ),
        migrations.AlterField(
            model_name='importlist',
            name='paid',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Paid'),
        ),
        migrations.AlterField(
            model_name='importlist',
            name='total',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='buy_price',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Buy price'),
        ),
        migrations.AlterField(
            model_name='importproduct',
            name='total_summ',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Total summ'),
        ),
        migrations.AlterField(
            model_name='lending',
            name='current_lending',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Current lending'),
        ),
        migrations.AlterField(
            model_name='lending',
            name='lending_amount',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Lending amount'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Amount'),
        ),
    ]
