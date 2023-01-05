from rest_framework.decorators import api_view
from base.models import Course, Rating
from .serializers import CourseSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from base.permissions import IsProfileOwner
from django.contrib.auth import get_user_model


@api_view(['GET'])
def getCourses(req):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCourse(req, code: str):
    course = Course.objects.get(code=code)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


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


@api_view(['GET'])
def getRating(req, id):
    rating = Rating.objects.get(id=id)
    serializer = RatingSerializer(rating)
    return Response(serializer.data)


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
