from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


class IsProfileOwner(BasePermission):
    """
    Allows access only to users who owns the profile.
    """

    def has_permission(self, request, view):
        return request.user == get_user_model().objects.get(id=view.kwargs['id'])
