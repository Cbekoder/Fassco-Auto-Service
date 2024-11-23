from decimal import Decimal
from django.db import models, transaction
from django.db.models import Sum, Case, When, F, DecimalField
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from users.models import Employee, Client
from inventory.models import Branch, Car, Service, Product


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=_('Car'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    overall_total = models.DecimalField(max_digits=15, decimal_places=0,  null=True)
    total = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Total'))
    paid = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Paid'))
    landing = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Debt'))
    product_total = models.DecimalField(default=0, max_digits=15, decimal_places=0, verbose_name=_('Product Total'))
    service_total = models.DecimalField(default=0, max_digits=15, decimal_places=0, verbose_name=_('Service Total'))

    odo_mileage = models.FloatField(blank=True, null=True, verbose_name=_('ODO mileage'))
    hev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('HEV mileage'))
    ev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('EV mileage'))

    start_date = models.DateField(null=True, verbose_name=_('Start date'))
    end_date = models.DateField(null=True, verbose_name=_('End date'))
    plan_date = models.DateField(null=True, verbose_name=_('Plan date'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Manager'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.description if self.description else f"{self.pk}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.client = self.car.client
            if self.manager and self.manager.position != "manager":
                raise ValidationError(f"Employee isn't manager")
            # if self.pk:
            #     old_instance = Order.objects.get(pk=self.pk)
            #     self.car.client.lending -= old_instance.landing
            #     self.branch.balance -= old_instance.paid

            today = timezone.now().date()
            if not self.start_date:
                self.start_date = today
            if not self.plan_date:
                self.plan_date = today
            if not self.end_date:
                self.end_date = self.start_date

            super().save(*args, **kwargs)

            self.car.client.lending += self.landing
            self.car.client.save()

            self.branch.balance += self.paid
            self.branch.save()

            if self.odo_mileage:
                self.car.odo_mileage = self.odo_mileage
            else:
                self.odo_mileage = self.car.odo_mileage
            if self.hev_mileage:
                self.car.hev_mileage = self.hev_mileage
            else:
                self.hev_mileage = self.car.hev_mileage
            if self.ev_mileage:
                self.car.ev_mileage = self.ev_mileage
            else:
                self.ev_mileage = self.car.ev_mileage
            self.car.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.client.lending -= self.landing
            self.client.save()

            self.branch.balance -= self.paid
            self.branch.save()

            super(Order, self).delete(*args, **kwargs)

ORDER_TYPES = (
    ('%', "Percentage"),
    ('$', "Money"),
)

class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Total'))
    discount_type = models.CharField(max_length=20, choices=ORDER_TYPES, default="%", verbose_name=_('Discount type'))
    discount = models.DecimalField(default=0, max_digits=15, decimal_places=0, verbose_name=_('Discount'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    part = models.FloatField(blank=True, null=True, verbose_name=_('Part'))
    mechanic = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name=_('Master'))

    class Meta:
        verbose_name = _('Order service')
        verbose_name_plural = _('Order services')

    def __str__(self):
        return f'{self.order.id} - {self.service.name}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # if self.pk:
            #     old_instance = OrderService.objects.get(pk=self.pk)
            #
            #     self.mechanic.balance -= self.mechanic.kpi * old_instance.part
            #
            #     if old_instance.discount_type == "%":
            #         current_total = old_instance.service.price * old_instance.part
            #         self.order.total -= current_total * (old_instance.discount / 100)
            #     elif old_instance.discount_type == "$":
            #         self.order.total -= old_instance.service.price * old_instance.part - old_instance.discount
            #     self.order.overall_total -= old_instance.service.price

            self.total = self.service.price * Decimal(self.part)
            if self.discount > 0:
                if self.discount_type == "%":
                    if 0 < self.discount < 100:
                        self.total -= self.total * self.discount / 100
                    else:
                        raise ValidationError({'detail': 'Discount amount must be from 0 to 100 if discout type is %'})
                if self.discount_type == "$":
                    if 0 < self.discount < self.service.price:
                        self.total -= self.discount
                    else:
                        raise ValidationError({'detail': 'If discount_type is $, Discount must be between 1000 and service.price'})

            super().save(*args, **kwargs)
            if self.mechanic:
                self.mechanic.balance += self.mechanic.kpi * Decimal(self.part)
                self.mechanic.save()

            self.order.total += self.total
            self.order.service_total += self.total
            self.order.overall_total += self.service.price * Decimal(self.part)
            self.order.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.mechanic.balance -= self.mechanic.kpi * Decimal(self.part)
            self.mechanic.save()

            if self.order:
                self.order.total -= self.total
                self.order.overall_total -= self.service.price * Decimal(self.part)
                self.order.save()

            super(OrderService, self).delete(*args, **kwargs)
            



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=1, verbose_name=_('Amount'))
    total = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Total'))
    discount_type = models.CharField(max_length=1, choices=ORDER_TYPES, default="%", verbose_name=_('Discount type'))
    discount = models.DecimalField(default=0, max_digits=15, decimal_places=0,verbose_name=_('Discount'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    warehouse_remainder = models.FloatField(default=0, blank=True, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')

    def __str__(self):
        return f'{self.order.id} - {self.product.name}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # if self.pk:
            #     old_instance = OrderProduct.objects.get(pk=self.pk)
            #
            #     self.product.amount += old_instance.amount
            #
            #     if old_instance.discount_type == "%" and 0 < self.discount <= 100:
            #         current_total = old_instance.amount * old_instance.product.sell_price
            #         self.order.total -= current_total * (old_instance.discount / 100)
            #     elif old_instance.discount_type == "$" and old_instance.discount <= old_instance.product.sell_price:
            #         self.order.total -= old_instance.amount * old_instance.product.sell_price - old_instance.discount
            #     self.order.overall_total -= old_instance.amount * old_instance.product.sell_price
            #
            #     manager.balance -= (manager.commission_per / 100) * old_instance.amount * (
            #                 self.product.sell_price - self.product.sell_price)

            self.total = Decimal(self.amount) * self.product.sell_price
            if self.discount > 0:
                if self.discount_type == "%":
                    if 0 < self.discount <= 100:
                        self.total -= self.total * (self.discount / 100)
                    else:
                        raise ValidationError({"detail": "Discount amount must be from 0 to 100 if discout type is %"})
                elif self.discount_type == "$":
                    if 0 < self.discount <= self.product.sell_price:
                        self.total -= self.discount
                    else:
                        raise ValidationError({"detail": "Discount amount must be from 0 to product sell price if discout type is $"})

            super().save(*args, **kwargs)
            if self.order.manager:
                manager = self.order.manager
                manager.balance += Decimal(manager.commission_per / 100) * Decimal(self.amount) * self.product.sell_price
                manager.save()

            warehouse_products = Product.objects.filter(branch=self.order.branch, is_temp=False)
            warehouse_total = warehouse_products.filter(amount__gt=0).aggregate(
                total_value=Sum(
                    F("amount") * F("sell_price"), output_field=DecimalField()))["total_value"] or 0
            self.warehouse_remainder = warehouse_total
            self.save()

            self.order.total += self.total
            self.order.product_total += self.total
            self.order.overall_total += Decimal(self.amount) * self.product.sell_price
            self.order.save()

            if self.product.amount >= self.amount:
                self.product.amount -= self.amount
                self.product.save()
            else:
                raise ValidationError(
                    f"Not enough product stock. Available: {self.product.amount}, requested: {self.amount}.")

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.product.amount += self.amount
            self.product.save()

            if self.order.manager:
                manager = self.order.manager
                manager.balance -= Decimal(manager.commission_per / 100) * Decimal(self.amount) * (
                        self.product.sell_price - self.product.arrival_price)
                manager.save()

            if self.order:
                self.order.total -= self.total
                self.order.overall_total -= Decimal(self.amount) * self.product.sell_price
                self.order.save()

            super(OrderProduct, self).delete(*args, **kwargs)
