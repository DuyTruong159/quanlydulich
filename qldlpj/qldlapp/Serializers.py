from django.utils.html import strip_tags
from django.db.models import Avg
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
    rate = SerializerMethodField()
    customer = SerializerMethodField()
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

    def get_rate(self,obj):
        average = obj.comments.all().aggregate(Avg('rating')).get('rating__avg')
        if average == None:
            return 0
        return int(average)

    def get_customer(self, obj):
        count = obj.comments.count()
        if count == None:
            return 0
        return count

    class Meta:
        model = Tour
        fields = ['id', 'name', 'image', 'description', 'city', 'datetime', 'duaration', 'stock', 'available', 'seats', 'tags', 'rate', 'customer']

class TagSerializer(ModelSerializer):
    tour = TourSerializer(many=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'tour']

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'avatar', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class CommentSerializer(ModelSerializer):
    user = UserSerializer()
    tour = 'TourSerializer()'

    class Meta:
        model = Comment
        fields = ['id', 'name', 'tour', 'user', 'rating', 'created_day']

class TicketSerializer(ModelSerializer):
    user = UserSerializer()
    tour = TourSerializer()
    seat = SeatSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'tour', 'seat', 'quantity', 'created_day']