from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from branches.models import Branch
from inventory.models import Product
from users.models import User, Employee, Supplier, Client


class BranchFundTransfer(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Daily fund amount'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Branch Fund')
        verbose_name_plural = _('Branch Funds')

    def __str__(self):
        return f'{self.branch_id.name} - {self.amount}'



class ExpenseType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense Type')
        verbose_name_plural = _('Expense Types')

    def __str__(self):
        return self.name


class Expense(models.Model):
    description = models.TextField(verbose_name=_('Description'))
    type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, verbose_name=_('Type'))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Amount'))
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return f"{self.type.name} - {self.description}"


class Salary(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'), related_name='for_employee')
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Amount'))
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Salary')
        verbose_name_plural = _('Salaries')

    def __str__(self):
        return f"{self.employee_id.first_name} - {self.description}"



class ImportList(models.Model):
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Total'))
    paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Paid'))
    debt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Debt'))
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Import list')
        verbose_name_plural = _('Import lists')

    def __str__(self):
        return f"{self.branch_id.name} - {self.description}"

class ImportProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    amount = models.FloatField(default=1, verbose_name=_('Debt'))
    buy_price = models.DecimalField(max_digits=15, decimal_places=2,verbose_name=_('Buy price'))
    total_summ = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Total summ'))
    import_list_id = models.ForeignKey(ImportList, on_delete=models.CASCADE, verbose_name=_('Import list'))

    class Meta:
        verbose_name = _('Import product')
        verbose_name_plural = _('Import products')

    def __str__(self):
        return f"{self.product_id.name} - {self.amount}"


class Debt(models.Model):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'), related_name='from_supplier')
    debt_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Debt amount'))
    is_debt = models.BooleanField(default=False, verbose_name=_('Is debt'))
    current_debt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Current debt'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Debt')
        verbose_name_plural = _('Debts')

    def __str__(self):
        return f"{self.supplier_id.first_name} - {self.debt_amount}"


class Lending(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client'), related_name="from_client")
    lending_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Lending amount'))
    is_lending = models.BooleanField(default=False, verbose_name=_('Is lending'))
    current_lending = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Current lending'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Lending')
        verbose_name_plural = _('Lendings')

    def __str__(self):
        return f"{self.client_id.first_name} - {self.lending_amount}"



