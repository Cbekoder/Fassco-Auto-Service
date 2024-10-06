from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models import Branch, Car, Service, Product


class Order(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    total = models.FloatField(default=0, verbose_name=_('Total'))
    paid = models.FloatField(default=0, verbose_name=_('Paid'))
    landing = models.FloatField(default=0, verbose_name=_('Debt'))

    odo_mileage = models.FloatField(blank=True, null=True, verbose_name=_('ODO mileage'))
    hev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('HEV mileage'))
    ev_mileage = models.FloatField(blank=True, null=True, verbose_name=_('EV mileage'))

    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.description


class OrderService(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    total = models.FloatField(default=0, verbose_name=_('Total'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Order service')
        verbose_name_plural = _('Order services')

    def __str__(self):
        return f'{self.order_id.description} - {self.service_id.name}'


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=1, verbose_name=_('Amount'))
    total = models.FloatField(default=0, verbose_name=_('Total'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')

    def __str__(self):
        return f'{self.order_id.description} - {self.product_id.name}'




