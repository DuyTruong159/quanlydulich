from django.utils.html import strip_tags
from rest_framework.serializers import ModelSerializer, SerializerMethodField, DateTimeField
from .models import *

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'name', 'price', 'tour']

class TourSerializer(ModelSerializer):
    image = SerializerMethodField()
    datetime = DateTimeField(format="%Y-%m-%d")
    seats = SeatSerializer(many=True)
    tags = 'TagSerializer(many=True)'

    def get_image(self, obj):
        request = self.context['request']
        name = obj.image.name
        path = "/static/%s" % name

        return request.build_absolute_uri(path)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['description'] = strip_tags(instance.description)
        return data

    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'description', 'city', 'datetime', 'duaration', 'stock', 'available', 'seats', 'tags']

class TagSerializer(ModelSerializer):
    tour = TourSerializer(many=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'tour']

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
