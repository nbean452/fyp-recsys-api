import pandas as pd
from django.contrib.auth.models import User
from django_pandas.io import read_frame
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.permissions import IsAccountOwner
from base.models import Course, Review, UserDetail

from .serializers import (CourseCreateSerializer, CourseViewSerializer,
                          ReviewCreateSerializer, ReviewViewSerializer,
                          UserDetailSerializer, UserDetailUpdateSerializer)

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


class CourseRecommendationView(generics.RetrieveAPIView):
    serializer_class = CourseViewSerializer
    lookup_field = "code"
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # if kwargs not found, return 404 not found!
        self.get_object()

        df = read_frame(self.queryset)
        # df.to_csv('tools/scraper/data.csv')
        # print(df.head()[['code', 'description']])

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

            sig_scores = sig_scores[1:4]

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


class ReviewListView(generics.ListAPIView):
    model = Review
    serializer_class = ReviewViewSerializer
    queryset = Review.objects.all()


class ReviewView(generics.RetrieveAPIView):
    serializer_class = ReviewViewSerializer
    lookup_field = 'id'
    queryset = Review.objects.all()


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


class ReviewUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    lookup_field = 'id'
    serializer_class = ReviewCreateSerializer


class ReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()
    lookup_field = 'id'


class UserDetailUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAccountOwner]
    queryset = UserDetail.objects.all()
    lookup_field = 'user__username'
    serializer_class = UserDetailUpdateSerializer


# class UserView(generics.RetrieveAPIView):
#     permission_classes = [IsAccountOwner | IsAdminUser]
#     model = User
#     serializer_class = UserDetailSerializer
#     lookup_field = 'username'
#     queryset = User.objects.all()


# class UserListView(generics.ListAPIView):
#     permission_classes = [IsAdminUser]
#     model = User
#     serializer_class = UserDetailSerializer
#     queryset = User.objects.all()
