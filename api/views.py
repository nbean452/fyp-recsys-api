import pandas as pd
from django.contrib.auth.models import User
from django_pandas.io import read_frame
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# TODO: figure out what is this! retrieve or list!


class CourseRecommendationView(generics.RetrieveAPIView):
    serializer_class = CourseViewSerializer
    lookup_field = "code"
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # if kwargs not found, return 404 not found!
        self.get_object()

        df = read_frame(self.queryset)
        # df.to_csv('tools/scraper/data.csv')
        print(df.head()[['code', 'description']])

        tfv = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                              ngram_range=(1, 3))

        tfv_matrix = tfv.fit_transform(df['description'])

        # Compute the similarity using cosine_similarity
        sig = cosine_similarity(tfv_matrix)

        indices = pd.Series(df.index,
                            index=df['code']).drop_duplicates()

        def make_recommendations(code, sig=sig):
            idx = indices[code]

            sig_scores = list(enumerate(sig[idx]))

            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

            sig_scores = sig_scores[1:11]

            course_indices = [i[0] for i in sig_scores]

            return df['code'].iloc[course_indices]

        recs = make_recommendations(kwargs['code'])

        recs_temp = {}

        for index, rec in enumerate(recs):
            recs_temp.update({rec: index})

        courses = Course.objects.filter(code__in=recs)

        courses = list(courses)
        courses.sort(key=lambda course: recs_temp[course.code])

        serializer = CourseViewSerializer(courses, many=True)

        return Response(serializer.data)


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
