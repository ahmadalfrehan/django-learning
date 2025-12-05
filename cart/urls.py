from django.urls import path
from .views import CartApi
urlpatterns = [
    path('api/carts',CartApi.as_view(),name='carts')
]