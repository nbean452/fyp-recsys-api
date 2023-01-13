from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """
    Allows access only to users who owns the profile.
    """

    def has_permission(self, request, view):
        return request.user == User.objects.get(username=view.kwargs['username'])
