from itertools import chain

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import *
from .Serializers import *
import random



# def index(request):
#     tour = Tour.objects.filter(available=True)
#     pagination = Paginator(tour, 8)
#     page_number = request.GET.get("page", 1)
#     try:
#         page_obj = pagination.page(page_number)
#     except PageNotAnInteger:
#         page_obj = pagination.page(1)
#     except EmptyPage:
#         page_obj = pagination.page(pagination.num_pages)
#
#     s = list(Tour.objects.filter(available=True))
#     s = random.sample(s, 3)
#     return render(request, template_name='index.html', context={"tour": page_obj, "ran": s})
#
#
# def aboutus(request):
#     return render(request, template_name='about_us.html')
#
#
# def mytour(request):
#     search = request.GET.get('kw')
#
#     try:
#         tboat = Tour.objects.filter(tags__name__icontains='Boat', available=True, name__icontains=search)
#         tboatran = list(tboat)
#         tboatcount = tboat.count()
#         tboatran = random.sample(tboatran, tboatcount)
#
#         tmountain = Tour.objects.filter(tags__name__icontains='Mountains', available=True, name__icontains=search)
#         tmountainran = list(tmountain)
#         tmountaincount = tmountain.count()
#         tmountainran = random.sample(tmountainran, tmountaincount)
#
#         tclimb = Tour.objects.filter(tags__name__icontains='Climbing', available=True, name__icontains=search)
#         tclimbran = list(tclimb)
#         tclimbcount = tclimb.count()
#         tclimbran = random.sample(tclimbran, tclimbcount)
#
#     except:
#         tboat = Tour.objects.filter(tags__name__icontains='Boat', available=True)
#         tboatran = list(tboat)
#         tboatcount = tboat.count()
#         tboatran = random.sample(tboatran, tboatcount)
#
#         tmountain = Tour.objects.filter(tags__name__icontains='Mountains', available=True)
#         tmountainran = list(tmountain)
#         tmountaincount = tmountain.count()
#         tmountainran = random.sample(tmountainran, tmountaincount)
#
#         tclimb = Tour.objects.filter(tags__name__icontains='Climbing', available=True)
#         tclimbran = list(tclimb)
#         tclimbcount = tclimb.count()
#         tclimbran = random.sample(tclimbran, tclimbcount)
#
#
#     seat1 = Seat.objects.filter(name__icontains='Adults')
#     seat2 = Seat.objects.filter(name__icontains='Childrens')
#
#     tag = Tag.objects.all()
#
#     tour = (tboat | tmountain | tclimb).distinct()
#     pagination = Paginator(tour, 6)
#     page_number = request.GET.get("page", 1)
#     try:
#         page_obj = pagination.page(page_number)
#     except PageNotAnInteger:
#         page_obj = pagination.page(1)
#     except EmptyPage:
#         page_obj = pagination.page(pagination.num_pages)
#
#     return render(request, template_name='tour.html',
#                   context={"tour": page_obj, "seat1": seat1, "seat2": seat2, "tag": tag, "tboat": tboatran,
#                            "tmountain": tmountainran, "tclimb": tclimbran})
#
# def tourinfo(request, id):
#     tour = Tour.objects.filter(pk=id)
#
#     seat1 = Seat.objects.filter(name__icontains='Adults')
#     seat2 = Seat.objects.filter(name__icontains='Childrens')
#
#     return render(request, template_name='tourinfo.html', context={"tour": tour, "seat1": seat1, "seat2": seat2})
#
# def customerprotec(request):
#     return render(request, template_name='customer_protection.html')
#
#
# def contact(request):
#     return render(request, template_name='contact.html')


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

    def get_queryset(self):
        tours = Tour.objects.filter(available=True)

        kw = self.request.query_params.get('kw')
        if kw is not None:
            tours = tours.filter(Q(name__icontains=kw) | Q(seats__price=kw))

        return tours

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

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
