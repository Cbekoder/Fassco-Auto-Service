from decimal import Decimal
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.db.models import Sum, Case, When, F, DecimalField
from branches.models import Branch, Wallet
from inventory.models import Product
from users.models import User, Employee, Supplier, Client


class Debt(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'),
                                 related_name='from_supplier')
    debt_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Debt amount'))
    is_debt = models.BooleanField(default=False, verbose_name=_('Is debt'))
    current_debt = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Current debt'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Debt')
        verbose_name_plural = _('Debts')

    def __str__(self):
        return f"{self.supplier.first_name} - {self.debt_amount}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            wallet = Wallet.objects.last()
            if self.pk:
                old_instance = Debt.objects.get(pk=self.pk)
                if self.is_debt:
                    self.supplier.debt -= old_instance.debt_amount
                    wallet -= old_instance.debt_amount
                else:
                    self.supplier.debt += old_instance.debt_amount
                    wallet += old_instance.debt_amount

            super().save(*args, **kwargs)

            if self.is_debt:
                self.supplier.debt += self.debt_amount
                wallet.balance += self.debt_amount
            else:
                if self.supplier.debt < self.debt_amount:
                    raise ValidationError({'detail': 'Paying debt amount is greater than branch debt from supplier'})
                wallet.balance -= self.debt_amount
                self.supplier.debt -= self.debt_amount
            self.supplier.save()


class ImportList(models.Model):
    total = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name=_('Total'))
    paid = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name=_('Paid'))
    debt = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name=_('Debt'))
    payment_type = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('Payment Type'))
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Supplier'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    is_initial_stock = models.BooleanField(default=False, verbose_name=_('Is Initial Stock'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Import list')
        verbose_name_plural = _('Import lists')

    def __str__(self):
        return f"{self.branch.name} - {self.description}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_initial_stock:
                self.paid = self.debt = self.payment_type = None
                super().save(*args, **kwargs)
            else:
                if self.payment_type == "0":
                    super().save(*args, **kwargs)
                else:
                    wallet = Wallet.objects.last()
                    if self.pk:
                        old_instance = ImportList.objects.get(pk=self.pk)
                        self.supplier.debt -= old_instance.debt
                        wallet.balance += old_instance.paid

                    super().save(*args, **kwargs)

                    self.supplier.debt += self.debt
                    wallet.balance -= self.paid

                    wallet.save()
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
    arrival_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Arrival price'))
    sell_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Sell price'))
    total_summ = models.DecimalField(max_digits=15, null=True, decimal_places=0, verbose_name=_('Total summ'))
    import_list = models.ForeignKey(ImportList, on_delete=models.CASCADE, verbose_name=_('Import list'))
    warehouse_remainder_sell_price = models.FloatField(default=0, blank=True,
                                                       verbose_name=_('Warehouse remainder sell price'))
    warehouse_remainder_arrival_price = models.FloatField(default=0, blank=True,
                                                          verbose_name=_('Warehouse remainder arrival price'))

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

            available = Product.objects.filter(name=self.product.name, is_temp=False)
            if available:
                wareProduct = available.last()
                wareProduct.amount += self.amount
                wareProduct.arrival_price = self.arrival_price
                wareProduct.sell_price = self.sell_price
                wareProduct.save()
            else:
                wareProduct = Product.objects.create(
                    code=self.product.code,
                    name=self.product.name,
                    amount=self.amount,
                    unit=self.product.unit,
                    arrival_price=self.arrival_price,
                    sell_price=self.sell_price,
                    min_amount=self.product.min_amount,
                    is_temp=False,
                    supplier=self.import_list.supplier,
                    branch=self.import_list.branch
                )
                self.product = wareProduct
            self.total_summ = self.arrival_price * Decimal(self.amount)

            warehouse_products = Product.objects.filter(branch=self.import_list.branch, is_temp=False)
            warehouse_total_sell = warehouse_products.filter(amount__gt=0).aggregate(
                total_value=Sum(
                    F("amount") * F("sell_price"), output_field=DecimalField()))["total_value"] or 0
            self.warehouse_remainder_sell_price = warehouse_total_sell + (
                    Decimal(self.amount) * self.product.sell_price)
            warehouse_total_arrival = warehouse_products.filter(amount__gt=0).aggregate(
                total_value=Sum(
                    F("amount") * F("arrival_price"), output_field=DecimalField()))["total_value"] or 0
            self.warehouse_remainder_arrival_price = warehouse_total_arrival + (
                    Decimal(self.amount) * self.product.arrival_price)

            super().save(*args, **kwargs)

            self.import_list.total += self.total_summ
            self.import_list.save()


class BranchFundTransfer(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Daily fund amount'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Branch Fund')
        verbose_name_plural = _('Branch Funds')

    def __str__(self):
        return f'{self.branch.name} - {self.amount}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            wallet = Wallet.objects.last()
            if self.branch.balance >= 0:
                wallet.balance += self.branch.balance
                wallet.save()
                self.branch.balance = 0
                self.branch.save()
            else:
                raise ValidationError({"detail": "Branch fund is less than 0"})


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
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Amount'))
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

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.branch.balance += self.amount
            self.branch.save()
            super(Expense, self).delete(*args, **kwargs)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_('Employee'),
                                 related_name='for_employee')
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Amount'))
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

            wallet.balance -= self.amount
            self.employee.balance -= self.amount

            self.employee.save()
            wallet.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            wallet = Wallet.objects.last()

            self.employee.balance += self.amount
            wallet.balance += self.amount

            self.employee.save()
            wallet.save()

            super(Salary, self).delete(*args, **kwargs)


class Lending(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client'), related_name="from_client")
    lending_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Lending amount'))
    is_lending = models.BooleanField(default=False, verbose_name=_('Is lending'))
    current_lending = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Current lending'))

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
                    self.branch.balance -= old_amount

            super().save(*args, **kwargs)

            if self.is_lending:
                self.client.lending += self.lending_amount
                self.branch.balance -= self.lending_amount
            else:
                if self.client.lending < self.lending_amount:
                    raise ValidationError({'detail': 'Lending amount is greater than client lending'})
                self.client.lending -= self.lending_amount
                self.branch.balance += self.lending_amount

            self.branch.save()
            self.client.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_lending:
                self.client.lending -= self.lending_amount
                self.branch.balance += self.lending_amount
            else:
                self.client.lending += self.lending_amount
                self.branch.balance -= self.lending_amount

            self.branch.save()
            self.client.save()

            super(Lending, self).delete(*args, **kwargs)
