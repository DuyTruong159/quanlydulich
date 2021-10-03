from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('City', views.CityViewSet)
router.register('TourHome', views.TourHomeViewSet)
router.register('Tour', views.TourViewSet, 'tour')
router.register('Seat', views.SeatViewSet)
router.register('Tag', views.TagViewSet)
router.register('User', views.UserViewSet)
router.register('Comment', views.CommentViewSet)
router.register('ticket', views.TicketViewSet, 'ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('oauth2-info/', views.AuthInfo.as_view())
]