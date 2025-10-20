from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and obj.is_published:
            return True
        
        if request.user and request.user.is_staff:
            return True

        return obj.user == request.user