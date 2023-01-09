from base.models import Course, Rating
from .serializers import CourseSerializer, RatingViewSerializer, RatingCreateSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from authentication.permissions import IsProfileOwner
from django.contrib.auth.models import User
from rest_framework import generics

# class-based views


class CourseListView(generics.ListAPIView):
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    lookup_field = "code"
    queryset = Course.objects.all()


class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    lookup_field = 'code'
    serializer_class = CourseSerializer


class CourseDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    lookup_field = 'code'


class RatingListView(generics.ListAPIView):
    model = Rating
    serializer_class = RatingViewSerializer
    queryset = Rating.objects.all()


class RatingView(generics.RetrieveAPIView):
    serializer_class = RatingViewSerializer
    lookup_field = 'id'
    queryset = Rating.objects.all()


class RatingCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer


class RatingUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Rating.objects.all()
    lookup_field = 'id'
    serializer_class = RatingCreateSerializer


class RatingDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Rating.objects.all()
    lookup_field = 'id'


class UserView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser | IsProfileOwner]
    serializer_class = UserSerializer
    lookup_field = 'username'
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()


# function-based views
# @api_view(['GET'])
# def getRatings(req):
#     ratings = Rating.objects.all()
#     serializer = RatingSerializer(ratings, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def addCourse(req):
#     serializer = CourseSerializer(data=req.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
