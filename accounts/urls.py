from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('weather/', WeatherUpdateView.as_view(), name='weather')
]
