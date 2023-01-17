from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from base.models import Course, Rating


class UserRatingSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        exclude = ['course']


class CourseViewSerializer(ModelSerializer):
    ratings = UserRatingSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'name', 'description',
                  'availability', 'is_active', 'created_at', 'updated_at', 'ratings']
        depth = 1


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'description',
                  'is_active', 'availability', 'created_at', 'updated_at']


class RatingViewSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        depth = 1


class RatingCreateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
