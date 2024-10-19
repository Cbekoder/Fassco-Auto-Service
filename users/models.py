from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from branches.models import Branch

class User(AbstractUser):
    branch = models.ForeignKey(Branch, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username


class UserTemp(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.TextField(null=True, blank=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Supplier(UserTemp):
    debt = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


POSITION_CHOICES = (
    ("manager", _("Manager")),
    ("mechanic", _("Mechanic")),
    ("other", _("Other")),
)

class Employee(UserTemp):
    position = models.CharField(max_length=15, choices=POSITION_CHOICES)
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    commission_per = models.IntegerField(default=2, null=True, blank=True)
    kpi = models.IntegerField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Client(UserTemp):
    lending = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name="client_lending")
    extra_phone = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"