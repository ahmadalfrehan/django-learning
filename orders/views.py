from django.shortcuts import render

from products.models import ProductVariant
from .serializers import OrderSerializer,OrderItemSerializer, PaymentSerializer #OrderSerializers, OrderItemSerializers
from .models import Order, OrderItem, Payment
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


@api_view(['POST'])
def pay_order(request, order_id):
    user = request.user

    # 1. Get the order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    # 2. Is order already paid?
    if hasattr(order, "payment") and order.payment.paid:
        return Response({"error": "Order already paid"}, status=400)

    # 3. Validate amount
    amount = request.data.get("amount")
    method = request.data.get("method")

    if float(amount) != float(order.total_price):
        return Response({"error": "Invalid amount"}, status=400)

    if method not in ["CARD", "COD"]:
        return Response({"error": "Invalid payment method"}, status=400)

    # 4. Create payment
    payment = Payment.objects.create(
        order=order,
        amount=amount,
        method=method,
        paid=True,  # sandbox mode: always true
        transaction_id=f"TX-{order.id}-{user.id}"
    )

    # 5. Mark order as paid
    order.status = "PAID"
    order.save()

    # 6. Send response
    serializer = PaymentSerializer(payment)
    return Response(serializer.data, status=201)
