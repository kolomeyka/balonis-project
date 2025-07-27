from django.urls import path
from . import views

urlpatterns = [
    # Зоны доставки
    path('delivery-zones/', views.DeliveryZoneListView.as_view(), name='delivery-zones'),
    
    # Заказы
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Утилиты
    path('calculate-cart/', views.calculate_cart, name='calculate-cart'),
    path('calculate-delivery/', views.calculate_delivery, name='calculate-delivery'),
]

