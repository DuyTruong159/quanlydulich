
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.conf import settings
from .Serializers import *
import random



class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class TourHomePagination(PageNumberPagination):
    page_size = 8

class TourPagination(PageNumberPagination):
    page_size = 6

class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    pagination_class = TourPagination

    def get_permissions(self):
        if self.action == 'add_comment':
            return [permissions.IsAuthenticated()]
        if self.action == 'add_ticket':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        tours = Tour.objects.filter(available=True)

        kw = self.request.query_params.get('kw')
        if kw is not None:
            tours = tours.filter(name__icontains=kw)

        return tours

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, pk):
        c = Comment.objects.filter(tour_id=pk)
        return Response(data=CommentSerializer(c, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add_comment')
    def add_comment(self, request, pk):
        content = request.data.get('name')
        rate = request.data.get('rating')
        try :
            c = Comment.objects.create(name=content,
                                       tour=self.get_object(),
                                       user=request.user,
                                       rating=rate)
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=True, url_path='add_ticket')
    def add_ticket(self, request, pk):
        quantity = request.data.get('quantity')
        # seat = request.data.get('seat')
        try:
            t = Ticket.objects.create(quantity=quantity,
                                      tour=self.get_object(),
                                      user=request.user
                                      )
            return Response(TicketSerializer(t).data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class TourHomeViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = TourHomePagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'get_tours_slide':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['post'], detail=True, url_path='hide_tour', url_name='hide_tour')
    def hide_tour(self, request, pk):
        try:
            t = Tour.objects.get(pk=pk)
            t.available = False
            t.save()
        except Tour.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=TourSerializer(t, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='open_tour', url_name='open_tour')
    def open_tour(self, request, pk):
        try:
            t = Tour.objects.get(pk=pk)
            t.available = True
            t.save()
        except Tour.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=TourSerializer(t, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='tour_slide')
    def get_tours_slide(self,request):
        t = Tour.objects.filter(available=True)
        t = random.sample(list(t), 3)
        s = t
        return Response(data=TourSerializer(s, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


