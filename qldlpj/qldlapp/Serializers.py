from rest_framework.serializers import ModelSerializer
from .models import *

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class TourSerializer(ModelSerializer):
    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'city', 'datetime', 'duaration', 'stock', 'available']

class SeatSerializer(ModelSerializer):
    tour = TourSerializer(many=True)
    class Meta:
        model = Seat
        fields = ['id', 'name', 'price', 'tour']