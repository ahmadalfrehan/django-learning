from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartSerializer
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer
from orders.serializers import OrderSerializer
from products.models import ProductVariant
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class CartApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddtoCartApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        variant_id = request.data.get("variant_id")
        quantity = request.data.get("quantity")
        if not variant_id:
            return Response({"Error": "variant id is required"}, status=status.HTTP_400_BAD_REQUEST)
        variant = get_object_or_404(ProductVariant, id=variant_id)
        if variant.stock < quantity:
            return Response({"Error": "not enough quantity"}, status=status.HTTP_400_BAD_REQUEST)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, varient=variant, defaults={"quantity": quantity})
        if not item_created:
            new_quantity = cart_item.quantity+quantity
            if variant.stock < new_quantity:
                return Response({"error": "NOT ENOUGH STOCK for this quantity"}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = new_quantity
            cart_item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes[IsAuthenticated]
def checkout(request):
    user = request.user
    variant_id = request.data.get("variant_id")
    quantity = request.data.get("quantity")
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    cart_item = cart.items.all()
    if not cart_item:
        return Response({"Error": "cart has not item"}, status=400)
    with transaction.atomic():
        for item in cart_item:
            if item.variant.stock < item.quantity:
                return Response({
                    "error": f"Not enough stock for {item.varient.product.name}"
                }, status=400)

        order = Order.objects.create(
            user=user,
            address=user.default_address,
            total_price=cart.total()
        )
        for item in cart_item:
            orderitem = OrderItem.objects.create(
                order=order,
                variant_id=item.variant,
                quantity=item.quantity,
                price=item.variant.price
            )

            item.variant.stock -= item.quantity
            item.variant.save()
        cart.items.all().delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=201)
