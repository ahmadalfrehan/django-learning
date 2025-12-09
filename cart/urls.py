from django.urls import path
from .views import CartApi, AddtoCartApi, checkout
urlpatterns = [
    # path('api/carts',CartApi.as_view(),name='carts'),

    path("add/", AddtoCartApi.as_view(), name="add-to-cart"),

    path('', CartApi.as_view()),
    path('checkout/', checkout),
]
