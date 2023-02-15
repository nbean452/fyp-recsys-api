from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ValidationError

from authentication.serializers import UserSerializer
from base.models import Course, Review, UserDetail


class UserDetailUpdateSerializer(ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        courses = Course.objects.filter(
            code__in=representation.get('taken_course'))

        representation['taken_course'] = CourseViewSerializer(
            courses, many=True).data

        return representation

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
    reviews = SerializerMethodField()

    def get_reviews(self, object):
        # get 10 similar stores for this store
        reviews = object.reviews.all()[:10]
        return UserReviewSerializer(reviews, many=True).data

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
    def validate(self, attrs):
        course = self.context['course']
        if Review.objects.filter(course=course, user=self.context['request'].user).exists():
            raise ValidationError(
                "This user has already added review for this course")
        return attrs

    class Meta:
        model = Review
        fields = '__all__'


class ReviewUpdateSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
