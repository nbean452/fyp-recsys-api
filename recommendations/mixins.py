import findspark
import pandas as pd
from django_pandas.io import read_frame
from pyspark.ml.recommendation import ALSModel, DataFrame
from pyspark.sql import SparkSession
from rest_framework import status
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from api.serializers import CourseViewSerializer
from base.models import Course


class CFMixin():
    def retrieve(self, request, *args, **kwargs):
        # if user not found, return 404 not found!
        self.get_object()

        # init spark
        findspark.init()
        SparkSession.builder\
            .master("local")\
            .appName("with-spark-recommender")\
            .getOrCreate()

        survey_ratings = pd.read_csv(
            'csv_data/survey_results.csv', index_col=False)
        app_ratings = pd.read_csv('csv_data/app_ratings.csv', index_col=False)
        course_ratings = pd.concat([app_ratings, survey_ratings])

        best_model = ALSModel.load('model/')

        user_recs = best_model.recommendForAllUsers(10)

        def make_recommendations(recs: DataFrame, user_id: int):
            # Recs should be a specific user, which is why filtering is needed
            filtered_recs = recs.filter(recs.user_id == user_id)

            # select the recommendations
            filtered_recs = filtered_recs.select(
                "recommendations.course_id", "recommendations.rating")
            courses_df = filtered_recs.select("course_id").toPandas()

            # if there is no data, return 0
            if len(courses_df) < 1:
                return 0

            courses = courses_df.iloc[0, 0]
            ratings_df = filtered_recs.select("rating").toPandas()
            ratings = ratings_df.iloc[0, 0]

            # use pandas dataframe as it's easier to add new columns, etc.
            ratings_matrix = pd.DataFrame(courses, columns=["course_id"])
            ratings_matrix["ratings"] = ratings
            ratings_matrix["user_id"] = user_id

            # remove courses already taken by users!
            selected_rows = course_ratings[course_ratings["user_id"] == user_id]
            course_ids = []

            for index, row in selected_rows.iterrows():
                course_ids.append(row["course_id"])

            ratings_matrix = ratings_matrix[ratings_matrix["course_id"].isin(
                course_ids) == False]

            return ratings_matrix["course_id"]

        recs = make_recommendations(user_recs, kwargs['id'])

        if type(recs) is int:
            return Response({"detail": "No data yet!"}, status=status.HTTP_404_NOT_FOUND)

        # queried courses needs to be sorted based on rating
        return Response(get_sorted_courses(recs, 'cf'))


class CBFMixin():
    def retrieve(self, request, *args, **kwargs):
        # if kwargs not found, return 404 not found!
        self.get_object()

        df = read_frame(self.queryset)

        tfv = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                              ngram_range=(1, 3))

        tfv_matrix = tfv.fit_transform(df['description'])

        # Compute the similarity using cosine_similarity
        sig = cosine_similarity(tfv_matrix)

        indices = pd.Series(df.index,
                            index=df['code']).drop_duplicates()

        def make_recommendations(sig, code):
            index = indices[code]

            sig_scores = list(enumerate(sig[index]))

            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

            sig_scores = sig_scores[1:4]

            course_indices = [i[0] for i in sig_scores]

            return df['code'].iloc[course_indices]

        recs = make_recommendations(sig, kwargs['code'])

        # queried courses needs to be sorted based on the likeliness
        return Response(get_sorted_courses(recs, 'cbf'))


def get_sorted_courses(recs: pd.Series, type: str):
    # queried courses needs to be sorted based on rating
    recs_temp = {}

    for index, rec in enumerate(recs):
        recs_temp.update({rec: index})

    if type == "cbf":
        courses = Course.objects.filter(code__in=recs)
    else:
        courses = Course.objects.filter(id__in=recs)

    courses = list(courses)
    if type == "cbf":
        courses.sort(key=lambda course: recs_temp[course.code])
    else:
        courses.sort(key=lambda course: recs_temp[course.id])

    return CourseViewSerializer(courses, many=True).data
