from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.serializers import (CourseCreateSerializer, CourseViewSerializer,
                             ReviewCreateSerializer, ReviewUpdateSerializer,
                             ReviewViewSerializer, UserDetailSerializer,
                             UserDetailUpdateSerializer)
from authentication.permissions import IsAccountOwner
from base.models import Course, Review, UserDetail
from recommendations.mixins import CBFMixin, CFMixin

# class-based views


class CourseListView(generics.ListAPIView):
    model = Course
    serializer_class = CourseViewSerializer

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


class CourseCBFRecommendationView(CBFMixin, generics.RetrieveAPIView):
    serializer_class = CourseViewSerializer
    lookup_field = "code"
    queryset = Course.objects.all()


class CourseCFRecommendationView(CFMixin, generics.RetrieveAPIView):
    # permission_classes = [IsAccountOwner]
    serializer_class = CourseViewSerializer
    lookup_field = "id"
    queryset = User.objects.all()


class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
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


class ReviewListView(generics.ListAPIView):
    model = Review
    serializer_class = ReviewViewSerializer
    queryset = Review.objects.all()


# class ReviewView(generics.RetrieveAPIView):
#     serializer_class = ReviewViewSerializer
#     lookup_field = 'id'
#     queryset = Review.objects.all()


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def get_serializer_context(self):
        return {'course': self.kwargs.get('id'), 'request': self.request, 'view': self, 'format': self.format_kwarg}


class ReviewUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    lookup_field = 'id'


# class ReviewDeleteView(generics.DestroyAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = Review.objects.all()
#     lookup_field = 'id'


class UserDetailUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAccountOwner]
    queryset = UserDetail.objects.all()
    lookup_field = 'user__username'
    serializer_class = UserDetailUpdateSerializer


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAccountOwner | IsAdminUser]
    model = User
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    queryset = User.objects.all()


# class UserListView(generics.ListAPIView):
#     permission_classes = [IsAdminUser]
#     model = User
#     serializer_class = UserDetailSerializer
#     queryset = User.objects.all()
