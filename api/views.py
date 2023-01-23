from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from authentication.permissions import IsProfileOwner
from base.models import Course, Rating

from .serializers import (CourseCreateSerializer, CourseViewSerializer,
                          RatingCreateSerializer, RatingViewSerializer,
                          UserSerializer)

# class-based views


class CourseListView(generics.ListAPIView):
    model = Course
    serializer_class = CourseViewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for key in serializer.data:
                key['availability'] = key['availability'].split(
                    ', ')
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for key in serializer.data:
            key['availability'] = key['availability'].split(
                ', ')
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Course.objects.all()
        filter = self.request.query_params.get('filter')

        if filter:
            queryset = queryset.filter(name__icontains=filter)
        return queryset


class CourseView(generics.RetrieveAPIView):
    serializer_class = CourseViewSerializer
    lookup_field = "code"
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        json_response = serializer.data

        json_response['availability'] = json_response['availability'].split(
            ', ')

        return Response(json_response)


class CourseRecommendationView(generics.RetrieveAPIView):
    serializer_class = CourseViewSerializer
    lookup_field = "code"
    queryset = Course.objects.all()


class CourseCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer


class CourseUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    lookup_field = 'code'
    serializer_class = CourseCreateSerializer


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
