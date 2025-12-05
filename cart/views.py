from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartSerializer
# Create your views here.


class CartApi(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors, status=400)

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
