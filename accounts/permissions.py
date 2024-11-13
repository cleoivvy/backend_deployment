from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    
    
    def has_permission(self, request, view):
        
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        else:
            raise PermissionDenied('You must be an admin to access this resource')