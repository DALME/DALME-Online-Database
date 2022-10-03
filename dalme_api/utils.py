from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Object-level permission to only allow owners of an object to edit it. """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.owner == request.user or request.user.is_superuser:
            return True
        else:
            return False
