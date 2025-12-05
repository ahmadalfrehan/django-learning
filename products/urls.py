from django.urls import path
from products.views import ProductCreate, ProductList,home,myvi, product_create_api, product_list_api


urlpatterns = [
    path("", ProductList.as_view(), name="product-list"),
    path("create", ProductCreate.as_view(), name="product-create"),
    path("home", home, name="produc"),
    path("myview",myvi),
    path("api/products/", product_list_api, name="product-list-api"),
    path("api/create_product/<int:pk>/", product_create_api, name="product-list-api"),
]
