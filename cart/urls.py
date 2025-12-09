from django.urls import path
from .views import CartApi,AddtoCartApi
urlpatterns = [
    path('api/carts',CartApi.as_view(),name='carts'),
    
    path("add/", AddtoCartApi.as_view(), name="add-to-cart"),
]