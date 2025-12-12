from .views import create_order, order_list,pay_order
from rest_framework.urls import path
urlpatterns = [
    path('api/order', create_order),
    path('api/orderlist', order_list),
    
    path("pay/<int:order_id>/", pay_order),
]
