from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee, Supplier, Client
from django.utils.translation import gettext_lazy as _

site.unregister(Group)

@register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'branch_id', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'branch_id__name')
    list_filter = ('branch_id', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        *UserAdmin.fieldsets,
        (  # new fieldset added on to the bottom
            _('Branch'),  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'branch_id',
                ),
            },
        ),
    )


@register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'branch_id', 'commission_per', 'salary', 'kpi')
    search_fields = ('first_name', 'last_name', 'branch_id__name', 'position')
    list_filter = ('branch_id', 'position')


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'branch_id', 'debt')
    search_fields = ('first_name', 'last_name', 'phone', 'branch_id__name')
    list_filter = ('branch_id',)


@register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'extra_phone', 'branch_id')
    search_fields = ('first_name', 'last_name', 'phone', 'extra_phone', 'branch_id__name')
    list_filter = ('branch_id',)


