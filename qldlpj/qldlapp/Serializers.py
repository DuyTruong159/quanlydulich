from rest_framework.serializers import ModelSerializer
from .models import *

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'name', 'price', 'tour']


class TagSerializer(ModelSerializer):
    tour = 'TourSerializer(many=True)'
    class Meta:
        model = Tag
        fields = ['id', 'name', 'tour']

class TourSerializer(ModelSerializer):
    seats = SeatSerializer(many=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'city', 'datetime', 'duaration', 'stock', 'available', 'seats', 'tags']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'avatar', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
