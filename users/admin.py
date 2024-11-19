from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee, Supplier, Client
from django.utils.translation import gettext_lazy as _

site.unregister(Group)

@register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'branch', 'is_staff', 'is_active')
    search_fields = ('username', 'branch__name')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'branch')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'branch')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'branch', 'password1', 'password2'),
        }),
    )
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined')


@register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'balance', 'position', 'branch', 'commission_per', 'salary', 'kpi')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'branch__name', 'position')
    list_filter = ('branch', 'position')


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'branch', 'debt')
    search_fields = ('first_name', 'last_name', 'phone', 'branch__name')
    list_filter = ('branch',)


@register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'lending', 'phone', 'extra_phone', 'branch')
    search_fields = ('first_name', 'last_name', 'phone', 'extra_phone', 'branch__name')
    list_filter = ('branch',)


