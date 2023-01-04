from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Course, Rating
from .serializers import CourseSerializer


@api_view(['GET'])
def getCourses(req):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addCourse(req):
    serializer = CourseSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
