from django.urls import path
from . import views

urlpatterns = [
    
    # Заказы
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Утилиты
    #path('calculate-cart/', views.calculate_cart, name='calculate-cart'),
    #path('calculate-delivery/', views.calculate_delivery, name='calculate-delivery'),
]

