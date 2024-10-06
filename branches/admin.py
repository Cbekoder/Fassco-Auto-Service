from django.contrib import admin
from .models import Wallet, Branch

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

    def has_add_permission(self, request):
        if Wallet.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'phone_number', 'address', 'created_at')  # Display fields in the list view
    search_fields = ('name', 'phone_number', 'address')  # Enable search by name and phone number
    # list_filter = ('created_at',)  # Add a filter for creation date
    ordering = ('-balance',)