from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from base.models import Course, Review


class UserReviewSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        exclude = ['course']


class CourseViewSerializer(ModelSerializer):
    reviews = UserReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'name', 'prerequisites', 'description',
                  'availability', 'is_active', 'reviews', 'created_at', 'updated_at']
        depth = 1


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'prerequisites', 'description',
                  'is_active', 'availability', 'created_at', 'updated_at']


class ReviewViewSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        depth = 1


class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
