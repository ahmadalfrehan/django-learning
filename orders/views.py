from django.shortcuts import render

from products.models import ProductVariant
from .serializers import OrderSerializer,OrderItemSerializer #OrderSerializers, OrderItemSerializers
from .models import Order, OrderItem
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.response import Response


from rest_framework import status
from django.views.generic.edit import CreateView
from rest_framework.decorators import api_view
# Create your views here.

from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    data = request.data
    items = data.pop('items')  # cart items

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            address_id=data.get('address'),
            coupon_id=data.get('coupon', None),
        )

        total = 0
        for item in items:
            variant = ProductVariant.objects.get(id=item['variant'])
            price = variant.price

            order_item = OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=item['quantity'],
                price=price
            )

            total += price * item['quantity']

        order.total_price = total
        order.save()

    return Response({"order_id": order.id}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
