from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from base.permissions import IsProfileOwner
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAdminUser | IsProfileOwner])
def getUser(req, id):
    user = get_user_model().objects.get(id=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(req):
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
