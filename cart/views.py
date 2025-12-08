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

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer
from products.models import ProductVariant


class CartApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
