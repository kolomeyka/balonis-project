from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import Order, OrderItem, DeliveryZone
from products.models import Product, Color, Size
from .serializers import (
    OrderSerializer, OrderCreateSerializer, DeliveryZoneSerializer,
    CartSerializer, CartItemSerializer
)


class DeliveryZoneListView(generics.ListAPIView):
    """Список зон доставки"""
    queryset = DeliveryZone.objects.filter(is_active=True)
    serializer_class = DeliveryZoneSerializer


class OrderCreateView(generics.CreateAPIView):
    """Создание заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Проверяем доступность товаров и корректность цен
        items_data = serializer.validated_data['items']
        total_calculated = 0
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'].id)
            
            # Проверяем, что цвет и размер доступны для товара
            if not product.colors.filter(id=item_data['selected_color'].id).exists():
                return Response(
                    {'error': f'Цвет недоступен для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not product.sizes.filter(id=item_data['selected_size'].id).exists():
                return Response(
                    {'error': f'Размер недоступен для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем количество
            if item_data['quantity'] < product.min_quantity or item_data['quantity'] > product.max_quantity:
                return Response(
                    {'error': f'Некорректное количество для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем цену
            expected_price = product.current_price
            if abs(float(item_data['price']) - float(expected_price)) > 0.01:
                return Response(
                    {'error': f'Некорректная цена для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            total_calculated += float(item_data['price']) * item_data['quantity']
        
        # Проверяем общую сумму
        if abs(float(serializer.validated_data['total_amount']) - total_calculated) > 0.01:
            return Response(
                {'error': 'Некорректная общая сумма заказа'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = serializer.save()
        
        # Возвращаем созданный заказ
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    """Детали заказа"""
    queryset = Order.objects.all().prefetch_related('items__product', 'items__selected_color', 'items__selected_size')
    serializer_class = OrderSerializer


@api_view(['POST'])
def calculate_cart(request):
    """Расчет стоимости корзины"""
    serializer = CartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    items_data = serializer.validated_data['items']
    cart_items = []
    total_amount = 0
    
    for item_data in items_data:
        try:
            product = Product.objects.get(id=item_data['product_id'], is_active=True)
            color = Color.objects.get(id=item_data['color_id'], is_active=True)
            size = Size.objects.get(id=item_data['size_id'], is_active=True)
            
            # Проверяем доступность цвета и размера для товара
            if not product.colors.filter(id=color.id).exists():
                return Response(
                    {'error': f'Цвет {color.name} недоступен для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not product.sizes.filter(id=size.id).exists():
                return Response(
                    {'error': f'Размер {size.name} недоступен для товара {product.name}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем количество
            quantity = item_data['quantity']
            if quantity < product.min_quantity or quantity > product.max_quantity:
                return Response(
                    {'error': f'Количество для товара {product.name} должно быть от {product.min_quantity} до {product.max_quantity}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            price = product.current_price
            item_total = price * quantity
            total_amount += item_total
            
            cart_items.append({
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'image': product.images.filter(is_main=True).first().image.url if product.images.filter(is_main=True).exists() else None
                },
                'color': {
                    'id': color.id,
                    'name': color.name,
                    'hex_code': color.hex_code
                },
                'size': {
                    'id': size.id,
                    'name': size.name,
                    'diameter': size.diameter
                },
                'quantity': quantity,
                'price': price,
                'total': item_total,
                'custom_text': item_data.get('custom_text', ''),
                'notes': item_data.get('notes', '')
            })
            
        except (Product.DoesNotExist, Color.DoesNotExist, Size.DoesNotExist) as e:
            return Response(
                {'error': 'Один из товаров не найден'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response({
        'items': cart_items,
        'total_amount': total_amount,
        'items_count': len(cart_items)
    })


@api_view(['POST'])
def calculate_delivery(request):
    """Расчет стоимости доставки"""
    zone_id = request.data.get('zone_id')
    total_amount = request.data.get('total_amount', 0)
    
    if not zone_id:
        return Response({'error': 'Не указана зона доставки'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        zone = DeliveryZone.objects.get(id=zone_id, is_active=True)
        
        # Проверяем минимальную сумму заказа
        if total_amount < zone.min_order_amount:
            return Response({
                'error': f'Минимальная сумма заказа для этой зоны: {zone.min_order_amount}₽',
                'min_order_amount': zone.min_order_amount
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'zone': DeliveryZoneSerializer(zone).data,
            'delivery_cost': zone.delivery_cost,
            'total_with_delivery': float(total_amount) + float(zone.delivery_cost)
        })
        
    except DeliveryZone.DoesNotExist:
        return Response({'error': 'Зона доставки не найдена'}, status=status.HTTP_404_NOT_FOUND)

