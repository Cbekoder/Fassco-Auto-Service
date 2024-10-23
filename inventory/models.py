from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import default
from django.utils.translation import gettext_lazy as _
from django.db import models

from branches.models import Branch
from users.models import Supplier, Client


class Product(models.Model):
    code = models.CharField(max_length=20, blank=False, null=False, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)],  verbose_name=_('Amount'))
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Unit'))
    arrival_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Import price'))
    sell_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Export price'))
    min_amount = models.FloatField(default=0, verbose_name=_('Min amount'))
    max_discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Max discount'))

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name



class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_('Price'))

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    brand = models.CharField(max_length=255, verbose_name=_('Brand'))
    color = models.CharField(max_length=20, verbose_name=_('Color'))
    state_number = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('State number'))
    vin_code = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('VIN code'))
    is_sold = models.BooleanField(default=False, verbose_name=_('Is sold'))

    odo_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('ODO mileage'))
    hev_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('HEV mileage'))
    ev_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('EV mileage'))

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        return self.name

















