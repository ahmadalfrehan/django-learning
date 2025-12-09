from cart.models import Cart, CartItem
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    variant_price = serializers.DecimalField(
        source='variant.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'variant_name',
                  'variant_price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ['id', 'user',  'created_at', 'session_id', 'items', 'total']

    def get_total(self, obj):
        return obj.total()
