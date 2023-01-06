from rest_framework.serializers import ModelSerializer
from base.models import Course, Rating
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class UserRatingSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        exclude = ['course']


class CourseSerializer(ModelSerializer):
    ratings = UserRatingSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'semester',
                  'is_active', 'created_at', 'updated_at', 'ratings']
        depth = 1


class RatingSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        depth = 1
