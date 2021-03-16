from django.urls import include, path
from .views import Home, create_match

urlpatterns = [
    path('', Home.as_view(), name='staff_home'),
    path('matches/add/', create_match, name='staff_create_match'),
]

