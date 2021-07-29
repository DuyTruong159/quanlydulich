from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .Serializers import *
import random

def index(request):
    tour = Tour.objects.filter(available=True)
    s = list(Tour.objects.filter(available=True))
    s = random.sample(s,3)
    return render(request, template_name='index.html', context={"tour": tour, "ran": s})

def aboutus(request):
    return render(request, template_name='about_us.html')

def mytour(request):
    return render(request, template_name='tour.html')

def customerprotec(request):
    return render(request, template_name='customer_protection.html')

def contact(request):
    return  render(request, template_name='contact.html')

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
