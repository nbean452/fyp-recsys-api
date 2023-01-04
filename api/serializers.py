from rest_framework.serializers import ModelSerializer
from base.models import Course, Rating


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
