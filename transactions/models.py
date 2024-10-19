from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from branches.models import Branch, Wallet
from inventory.models import Product
from users.models import User, Employee, Supplier, Client


class Debt(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'), related_name='from_supplier')
    debt_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Debt amount'))
    is_debt = models.BooleanField(default=False, verbose_name=_('Is debt'))
    current_debt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Current debt'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Debt')
        verbose_name_plural = _('Debts')

    def __str__(self):
        return f"{self.supplier.first_name} - {self.debt_amount}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = Debt.objects.get(pk=self.pk)
                if self.is_debt:
                    self.supplier.debt += old_instance.debt_amount
                else:
                    self.branch.balance -= old_instance.debt_amount
                    self.supplier.debt -= old_instance.debt_amount

            super().save(*args, **kwargs)

            if self.is_debt:
                self.supplier.debt += self.debt_amount
            else:
                if self.supplier.debt < self.debt_amount:
                    raise ValidationError({'detail':'Paying debt amount is greater than branch debt from supplier'})
                if self.branch.balance < self.debt_amount:
                    raise ValidationError({'detail':'Not enough balance to pay debt amount'})
                self.branch.balance -= self.debt_amount
                self.supplier.debt -= self.debt_amount
            self.supplier.save()
            self.branch.save()



class ImportList(models.Model):
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Total'))
    paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Paid'))
    debt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Debt'))
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Import list')
        verbose_name_plural = _('Import lists')

    def __str__(self):
        return f"{self.branch.name} - {self.description}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = ImportList.objects.get(pk=self.pk)
                old_debt = old_instance.debt
                self.supplier.debt -= old_debt
            self.debt = self.total - self.paid
            super().save(*args, **kwargs)

            self.supplier.debt += self.debt
            self.supplier.save()

    # def delete(self, *args, **kwargs):
    #     with transaction.atomic():
    #         self.import_list.total -= self.total_summ
    #         self.import_list.save()
    #
    #         # Now delete the ImportListProductt instance
    #         super().delete(*args, **kwargs)

class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    amount = models.FloatField(default=1, verbose_name=_('Debt'))
    buy_price = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_('Buy price'))
    total_summ = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Total summ'))
    import_list = models.ForeignKey(ImportList, on_delete=models.CASCADE, verbose_name=_('Import list'))

    class Meta:
        verbose_name = _('Import product')
        verbose_name_plural = _('Import products')

    def __str__(self):
        return f"{self.product.name} - {self.amount}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = ImportProduct.objects.get(pk=self.pk)
                old_total_summ = old_instance.total_summ
                old_amount = old_instance.amount
                self.product.amount -= old_amount
                self.import_list.total -= old_total_summ

            if self.product.arrival_price != self.buy_price:
                existint_product = Product.objects.filter(
                    name=self.product.name,
                    branch=self.product.branch,
                    supplier=self.product.supplier,
                    arrival_price=self.buy_price
                )
                if existint_product:
                    self.product = existint_product.last()
                else:
                    new_product = Product.objects.create(
                        name=self.product.name,
                        code=self.product.code,
                        amount=0,
                        unit=self.product.unit,
                        arrival_price=self.buy_price,
                        sell_price=self.product.sell_price,
                        branch=self.product.branch,
                        supplier=self.product.supplier
                    )
                    self.product = new_product

            self.total_summ = self.buy_price * Decimal(self.amount)

            super().save(*args, **kwargs)

            self.import_list.total += self.total_summ
            self.product.amount += self.amount

            self.product.save()
            self.import_list.save()


class BranchFundTransfer(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Daily fund amount'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Branch Fund')
        verbose_name_plural = _('Branch Funds')

    def __str__(self):
        return f'{self.branch.name} - {self.amount}'



class ExpenseType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense Type')
        verbose_name_plural = _('Expense Types')

    def __str__(self):
        return self.name


class Expense(models.Model):
    description = models.TextField(verbose_name=_('Description'))
    type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, verbose_name=_('Type'))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Amount'))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return f"{self.type.name} - {self.description}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = Expense.objects.get(pk=self.pk)
                old_amount = old_instance.amount
                self.branch.balance += old_amount
            super().save(*args, **kwargs)
            if self.branch.balance >= self.amount:
                self.branch.balance -= self.amount
            else:
                raise ValidationError({'detail': 'Not enough balance to spend expense amount'})
            self.branch.save()


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'), related_name='for_employee')
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Amount'))
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')

    def __str__(self):
        return f"{self.employee.first_name} - {self.description}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            wallet = Wallet.objects.last()
            if self.pk:
                old_instance = Salary.objects.get(pk=self.pk)
                old_amount = old_instance.amount
                wallet.balance += old_amount
                self.employee.balance += old_amount
            super().save(*args, **kwargs)
            if self.employee.balance >= self.amount:
                wallet.balance -= self.amount
                self.employee.balance -= self.amount
                self.employee.save()
                wallet.save()
            else:
                raise ValidationError({'detail': 'Not enough balance to spend salary amount'})



class Lending(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client'), related_name="from_client")
    lending_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Lending amount'))
    is_lending = models.BooleanField(default=False, verbose_name=_('Is lending'))
    current_lending = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Current lending'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Lending')
        verbose_name_plural = _('Lendings')

    def __str__(self):
        return f"{self.client.first_name} - {self.lending_amount}"


    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = Lending.objects.get(pk=self.pk)
                old_amount = old_instance.lending_amount
                if old_instance.is_lending:
                    self.client.lending -= old_amount
                else:
                    self.client.lending += old_amount
                    self.branch -= old_amount

            super().save(*args, **kwargs)

            if self.is_lending:
                self.client.lending += self.lending_amount
            else:
                if self.client.lending < self.lending_amount:
                    raise ValidationError({'detail': 'Lending amount is greater than client lending'})
                self.client.lending -= self.lending_amount
                self.branch += self.lending_amount

            self.branch.save()
            self.client.save()


