from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework.exceptions import ValidationError


class Wallet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallet')

    def save(self, *args, **kwargs):
        if not self.pk and Wallet.objects.exists():
            raise ValidationError(_('There can be only one Wallet instance.'))
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.balance)


class Branch(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('Phone number'))
    balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_('Balance'), default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Branch ')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return self.name


