from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from base.models import Course, Review, UserDetail


class UserDetailUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['taken_course']


class UserDetailSerializer(ModelSerializer):

    def to_representation(self, instance):
        """Move fields from detail to user representation."""
        representation = super().to_representation(instance)
        detail_representation: dict = representation.pop('detail')
        detail_representation.pop('user')
        for key in detail_representation:
            representation[key] = detail_representation[key]

        courses = Course.objects.filter(
            code__in=representation['taken_course'])

        data = CourseViewSerializer(courses, many=True).data

        representation['taken_course'] = data

        return representation

    class Meta:
        model = User
        fields = ['id', 'username', 'detail', 'is_superuser', 'first_name',
                  'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login']
        depth = 1


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
