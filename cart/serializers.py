from cart.models import Cart
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'quantity', 'total']

    def get_total(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'created_at']

    def get_total(self, obj):
        return obj.total()
