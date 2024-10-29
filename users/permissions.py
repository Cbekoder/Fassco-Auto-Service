from rest_framework.permissions import BasePermission


class IsSameBranch(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.branch_id == obj.branch_id

class IsSuperStatus(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if not request.user.is_superuser and not request.user.is_staff:
                return True
        return False