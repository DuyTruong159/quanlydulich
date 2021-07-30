from rest_framework.serializers import ModelSerializer
from .models import *

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class TourSerializer(ModelSerializer):
    seats = 'SeatSerializer(many=True)'
    tags = 'TagSerializer(many=True)'
    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'city', 'datetime', 'duaration', 'stock', 'available', 'seats', 'tags']

class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'name', 'price', 'tour']

class TagSerializer(ModelSerializer):
    tour = TourSerializer(many=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'tour']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'avatar']