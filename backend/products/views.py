from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Min, Max
from .models import Category, Color, Source, Product
from .serializers import (
    CategorySerializer, ColorSerializer, SourceSerializer,
    ProductListSerializer, ProductDetailSerializer, 
    ProductCreateSerializer
)


class CategoryListView(generics.ListAPIView):
    """Список категорий"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ColorListView(generics.ListAPIView):
    """Список цветов"""
    queryset = Color.objects.filter(is_active=True)
    serializer_class = ColorSerializer


class SourceListView(generics.ListAPIView):
    """Список источников материалов"""
    queryset = Source.objects.filter(is_active=True)
    serializer_class = SourceSerializer


class ProductListView(generics.ListAPIView):
    """Список товаров с фильтрацией"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'colors', 'sources', 'shape', 'theme', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['created_at', 'base_price', 'views_count', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_price__lte=max_price)
            
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Детальная информация о товаре"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Увеличиваем счетчик просмотров
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedProductsView(generics.ListAPIView):
    """Рекомендуемые товары"""
    queryset = Product.objects.filter(is_active=True, is_featured=True).select_related('category')
    serializer_class = ProductListSerializer


class PopularProductsView(generics.ListAPIView):
    """Популярные товары (по просмотрам)"""
    queryset = Product.objects.filter(is_active=True).select_related('category').order_by('-views_count')[:10]
    serializer_class = ProductListSerializer


class ProductCreateView(generics.CreateAPIView):
    """Создание товара (для админки)"""
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


# class ReviewListCreateView(generics.ListCreateAPIView):
#     """Список и создание отзывов"""
#     serializer_class = ReviewSerializer
#
#     def get_queryset(self):
#         product_id = self.kwargs.get('product_id')
#         return Review.objects.filter(product_id=product_id, is_approved=True).order_by('-created_at')
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return ReviewCreateSerializer
#         return ReviewSerializer


@api_view(['GET'])
def product_filters(request):
    """Получение всех доступных фильтров"""
    categories = Category.objects.filter(is_active=True)
    colors = Color.objects.filter(is_active=True)
    sources = Source.objects.filter(is_active=True)
    
    # Получаем диапазон цен
    products = Product.objects.filter(is_active=True)
    price_range = products.aggregate(min_price=Min('base_price'), max_price=Max('base_price'))
    min_price = price_range['min_price'] or 0
    max_price = price_range['max_price'] or 0
    
    shapes = [{'value': choice[0], 'label': choice[1]} for choice in Product.SHAPE_CHOICES]
    themes = [{'value': choice[0], 'label': choice[1]} for choice in Product.THEME_CHOICES]
    
    return Response({
        'categories': CategorySerializer(categories, many=True).data,
        'colors': ColorSerializer(colors, many=True).data,
        'sources': SourceSerializer(sources, many=True).data,
        'shapes': shapes,
        'themes': themes,
        'price_range': {
            'min': min_price,
            'max': max_price
        }
    })


@api_view(['GET'])
def search_products(request):
    """Поиск товаров"""
    query = request.GET.get('q', '')
    if not query:
        return Response({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(short_description__icontains=query),
        is_active=True
    ).select_related('category')[:20]
    
    serializer = ProductListSerializer(products, many=True)
    return Response({'results': serializer.data})

