from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """
    Allows access only to users who owns the account.
    """

    def has_permission(self, request, view):
        username = view.kwargs.get(
            'username') or view.kwargs.get('user__username') or view.kwargs.get('id')
        return request.user == User.objects.get(username=username)
