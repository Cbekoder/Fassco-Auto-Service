from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from branches.models import Branch
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
                old_total_summ = old_instance.total_summ
                self.total -= old_total_summ
                old_debt = old_instance.debt
                self.supplier.debt -= old_debt

            self.total_summ = self.buy_price * self.amount

            super().save(*args, **kwargs)

            self.supplier.debt += self.debt
            self.import_list.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.import_list.total -= self.total_summ
            self.import_list.save()

            # Now delete the ImportListProductt instance
            super().delete(*args, **kwargs)

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

            self.total_summ = self.buy_price * self.amount

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
            self.branch.balance -= self.amount
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



