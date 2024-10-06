from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

class Wallet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    balance = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.balance)

class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))
    balance = models.FloatField(verbose_name=_('Balance'), default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Branch ')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return self.name


