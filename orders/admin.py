from django.contrib import admin
from .models import Coupon, Order, OrderItem, Payment
# Register your models here.
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
