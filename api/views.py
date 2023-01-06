from rest_framework.decorators import api_view
from base.models import Course, Rating
from .serializers import CourseSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from base.permissions import IsProfileOwner
from django.contrib.auth.models import User
from rest_framework import generics


class CourseListView(generics.ListAPIView):
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    # permission_classes = (IsAuthenticated)
    lookup_field = "code"
    queryset = Course.objects.all()


@api_view(['POST'])
def addCourse(req):
    serializer = CourseSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getRatings(req):
    ratings = Rating.objects.all()
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)


class RatingView(generics.RetrieveAPIView):
    serializer_class = RatingSerializer
    lookup_field = 'id'
    queryset = Rating.objects.all()


@api_view(['GET'])
@permission_classes([IsAdminUser | IsProfileOwner])
def getUser(req, id):
    user = User.objects.get(id=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(req):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


class UserView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser | IsProfileOwner]
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
