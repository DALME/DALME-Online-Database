from rest_framework import permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response


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


def DTE_exception_handler(exc, context):
    if isinstance(exc, PermissionDenied):
        return Response({'detail': exc.detail}, 400)
    if isinstance(exc, ValidationError):
        fieldErrors = []
        errors = exc.detail
        for k, v in errors.items():
            if type(v) is dict:
                for k2, v2 in v.items():
                    field = k+'.'+k2
                    try:
                        fieldErrors.append({'name': field, 'status': str(v2[0])})
                    except KeyError:
                        fieldErrors.append({'name': field, 'status': errors})
            else:
                field = k
                fieldErrors.append({'name': field, 'status': str(v[0])})
        return Response({'fieldErrors': fieldErrors}, 400)
    else:
        return None
