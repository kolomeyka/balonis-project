from rest_framework import serializers
from .models import Order, OrderItem, DeliveryZone
from products.models import Product, Color
from products.serializers import ProductListSerializer, ColorSerializer


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = ['id', 'name', 'description', 'delivery_cost', 'min_order_amount']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    selected_color = ColorSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'selected_color',
            'custom_text', 'quantity', 'price', 'total_price', 'notes'
        ]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product', 'selected_color',
            'custom_text', 'quantity', 'price', 'notes'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_with_delivery = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'delivery_date', 'delivery_time',
            'status', 'status_display', 'payment_method', 'payment_method_display',
            'total_amount', 'delivery_cost', 'total_with_delivery',
            'notes', 'items', 'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'delivery_date', 'delivery_time',
            'payment_method', 'total_amount', 'delivery_cost',
            'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class CartItemSerializer(serializers.Serializer):
    """Сериализатор для элемента корзины"""
    product_id = serializers.IntegerField()
    color_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    custom_text = serializers.CharField(max_length=200, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Товар не найден")
    
    def validate_color_id(self, value):
        try:
            Color.objects.get(id=value, is_active=True)
            return value
        except Color.DoesNotExist:
            raise serializers.ValidationError("Цвет не найден")


class CartSerializer(serializers.Serializer):
    """Сериализатор для корзины"""
    items = CartItemSerializer(many=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Корзина не может быть пустой")
        return value

