from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products.models import Product, Color  # Убрал Size из импорта
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer


class OrderListView(generics.ListAPIView):
    """
    Список всех заказов
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    """
    Детали конкретного заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    """
    Создание нового заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        # Можно добавить дополнительную логику при создании заказа
        serializer.save()


@api_view(['GET'])
def order_status_choices(request):
    """
    Возвращает доступные статусы заказов
    """
    choices = [
        {'value': choice[0], 'label': choice[1]}
        for choice in Order.STATUS_CHOICES
    ]
    return Response(choices)


@api_view(['POST'])
def create_order_from_cart(request):
    """
    Создание заказа из корзины
    """
    try:
        # Получаем данные из запроса
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')
        customer_phone = request.data.get('customer_phone')
        delivery_address = request.data.get('delivery_address')
        cart_items = request.data.get('cart_items', [])

        if not cart_items:
            return Response(
                {'error': 'Корзина пуста'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем заказ
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            status='pending'
        )

        total_amount = 0

        # Создаем элементы заказа
        for item in cart_items:
            product = get_object_or_404(Product, id=item['product_id'])
            quantity = item['quantity']
            
            # Убрал логику с размерами, так как Size больше нет
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            total_amount += product.price * quantity

        # Обновляем общую сумму заказа
        order.total_amount = total_amount
        order.save()

        # Возвращаем созданный заказ
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PATCH'])
def update_order_status(request, order_id):
    """
    Обновление статуса заказа
    """
    try:
        order = get_object_or_404(Order, id=order_id)
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Недопустимый статус'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

