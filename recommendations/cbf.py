import pandas as pd
from django_pandas.io import read_frame
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from api.serializers import CourseViewSerializer
from base.models import Course


class CBFMixin():
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
