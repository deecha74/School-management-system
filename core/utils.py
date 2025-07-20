from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return  hasattr(request.user, 'role') and request.user.role == 'admin'


class IsTeacherUser(BasePermission):
    """
    Custom permission to only allow teacher users to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'teacher' role
        return hasattr(request.user, 'role') and request.user.role == 'teacher'

