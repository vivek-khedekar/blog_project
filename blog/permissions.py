from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow read-only requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE methods always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin can edit/delete anything
        if request.user.role == "admin":
            return True

        # Author can edit/delete their own stuff
        return obj.author == request.user
