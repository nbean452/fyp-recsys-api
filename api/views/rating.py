from rest_framework.decorators import api_view
from base.models import Rating
from ..serializers import RatingSerializer
from rest_framework.response import Response


@api_view(['GET'])
def getRatings(req):
    ratings = Rating.objects.all()
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRating(req, id):
    rating = Rating.objects.get(id=id)
    serializer = RatingSerializer(rating)
    return Response(serializer.data)
