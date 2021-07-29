from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('City', views.CityViewSet)
router.register('Tour', views.TourViewSet)
router.register('Seat', views.SeatViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('about_us/', views.aboutus, name='aboutus'),
    path('tour_list/', views.mytour, name='tourlist'),
    path('customer_protect/', views.customerprotec, name='customerprotec'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin_site.urls),
]