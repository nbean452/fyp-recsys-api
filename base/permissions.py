from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsProfileOwner(BasePermission):
    """
    Allows access only to users who owns the profile.
    """

    def has_permission(self, request, view):
        return request.user == User.objects.get(id=view.kwargs['id'])
