from rest_framework.permissions import BasePermission


class IsSameBranch(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.branch_id == obj.branch_id

class IsSuperStatus(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsStaffStatus(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_staff or request.user.is_superuser