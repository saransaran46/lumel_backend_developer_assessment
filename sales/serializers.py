from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer()
    
    class Meta:
        model = Order
        fields = '__all__'

class RevenueAnalysisSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    group_by = serializers.ChoiceField(
        choices=['product', 'category', 'region', None],
        required=False,
        allow_null=True
    )

class TopProductsSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    limit = serializers.IntegerField(min_value=1, max_value=100, default=10)
    category = serializers.CharField(required=False, allow_null=True)
    region = serializers.CharField(required=False, allow_null=True)