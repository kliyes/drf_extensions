from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission, SAFE_METHODS


UserModel = get_user_model()


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Ref: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        if isinstance(obj, UserModel):
            return obj == request.user
        return obj.user == request.user


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Ref: http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#object-level-permissions
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, UserModel):
            return obj == request.user
        return obj.user == request.user
