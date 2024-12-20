from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import default
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from branches.models import Branch
from users.models import Supplier, Client


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True, verbose_name=_('Amount'))
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Unit'))
    arrival_price = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name=_('Import price'))
    sell_price = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name=_('Export price'))
    min_amount = models.FloatField(default=0, verbose_name=_('Min amount'))
    is_temp = models.BooleanField(default=True, null=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Supplier'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_temp:
                instances = Product.objects.filter(name=self.name, is_temp=True)
                if instances:
                    raise ValidationError({'detail': "You cannot create two temp product with same name"})
            super().save(*args, **kwargs)


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
    vin_code = models.CharField(max_length=30, blank=True, null=True, unique=True, verbose_name=_('VIN code'))
    is_sold = models.BooleanField(default=False, verbose_name=_('Is sold'))

    odo_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('ODO mileage'))
    hev_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('HEV mileage'))
    ev_mileage = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_('EV mileage'))
    year_manufacture = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Year manufacture'))

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name=_('Client id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('Branch'))

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self):
        return self.name

















