from django.urls import path

from .views import login, register_api

urlpatterns = [
    path('login', login, name='login'),
    path('api/register/', register_api),
]
