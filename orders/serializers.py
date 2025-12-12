from rest_framework import serializers
from .models import Order, OrderItem, Payment

from products.models import ProductVariant
class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'variant', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.price * obj.quantity


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    variants = VariantSerializer()
    orderITem = OrderItemSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'address',
            'status',
            'coupon',
            'total_price',
            'created_at',
            'variants',
            'items',
            'orderITem'
        ]
        read_only_fields = ['total_price', 'status']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = '__all__'