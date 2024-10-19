from decimal import Decimal
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from users.models import Employee
from inventory.models import Branch, Car, Service, Product


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=_('Car'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    total = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2, verbose_name=_('Total'))
    paid = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2, verbose_name=_('Paid'))
    landing = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2, verbose_name=_('Debt'))

    odo_mileage = models.FloatField(blank=True, null=True, verbose_name=_('ODO mileage'))
    hev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('HEV mileage'))
    ev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('EV mileage'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name=_('Manager'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = Order.objects.get(pk=self.pk)
                self.car.client.lending -= old_instance.landing
                self.branch.balance -= old_instance.paid

            super().save(*args, **kwargs)

            self.car.client.lending += self.landing
            self.car.client.save()

            self.branch.balance += self.paid
            self.branch.save()

            if self.odo_mileage:
                self.car.odo_mileage = self.odo_mileage
                self.car.save()
            if self.hev_mileage:
                self.car.hev_mileage = self.hev_mileage
                self.car.save()
            if self.ev_mileage:
                self.car.ev_mileage = self.ev_mileage
                self.car.save()


class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2, verbose_name=_('Total'))
    discount = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2,
                                   verbose_name=_('Discount'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    part = models.FloatField(blank=True, null=True, verbose_name=_('Part'))
    mechanic = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name=_('Master'))

    class Meta:
        verbose_name = _('Order service')
        verbose_name_plural = _('Order services')

    def __str__(self):
        return f'{self.order.description} - {self.service.name}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = OrderService.objects.get(pk=self.pk)
                self.mechanic.balance -= self.mechanic.kpi * old_instance.part
            super().save(*args, **kwargs)
            self.mechanic.balance += self.mechanic.kpi * self.part
            self.mechanic.save()
            



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=1, verbose_name=_('Amount'))
    total = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2, verbose_name=_('Total'))
    discount = models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2,
                                   verbose_name=_('Discount'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')

    def __str__(self):
        return f'{self.order.description} - {self.product.name}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_instance = OrderProduct.objects.get(pk=self.pk)
                self.product.amount += old_instance.amount

                manager = self.order.manager
                manager.balance -= (manager.commission_per / 100) * old_instance.amount * (
                            self.product.sell_price - self.product.sell_price)

            if self.total != self.amount * self.product.sell_price:
                self.total = self.amount * self.product.sell_price

            super().save(*args, **kwargs)

            manager = self.order.manager
            manager.balance += (manager.commission_per / 100) * self.amount * (self.product.sell_price - self.product.sell_price)
            manager.save()

            if self.product.amount >= self.amount:
                self.product.amount -= self.amount
                self.product.save()
            else:
                raise ValidationError(
                    f"Not enough product stock. Available: {self.product.amount}, requested: {self.amount}.")
