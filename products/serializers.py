from rest_framework import serializers
from .models import Product, ProductVariant, Category
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'