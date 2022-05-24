"""
Defines custom permissions for Django REST Framework
"""
from rest_framework import permissions

from .models import Event
from .helpers import is_attending_user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Sourced from https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so GET, HEAD or OPTIONS requests will always be allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the owner of the object is allowed write permission
        return obj.owner == request.user

class IsParticipating(permissions.BasePermission):
    """
    Custom permission to only allow owners or participants of
    Sourced from https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    """

    def has_permission(self, request, view):
        try:
            event = Event.objects.get(pk=view.kwargs['pk'])
            return is_attending_user(request.user, event)
        except Event.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        return is_attending_user(request.user, obj)
