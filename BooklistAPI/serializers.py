from rest_framework import serializers
from .models import BookItem, Category
from decimal import Decimal

# class BookItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class BookItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source = 'inventory') # This simply changes the name of a field and must be added to the fields section
    price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = BookItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']

    def calculate_tax(self, product:BookItem):
        return product.price * Decimal(1.1)
