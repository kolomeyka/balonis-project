from rest_framework import generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import GalleryCategory, GalleryImage, ClientReview
from .serializers import (
    GalleryCategorySerializer, GalleryImageSerializer, 
    GalleryImageListSerializer, ClientReviewSerializer,
    ClientReviewCreateSerializer
)


class GalleryCategoryListView(generics.ListAPIView):
    """Список категорий галереи"""
    queryset = GalleryCategory.objects.filter(is_active=True)
    serializer_class = GalleryCategorySerializer


class GalleryImageListView(generics.ListAPIView):
    """Список изображений галереи"""
    queryset = GalleryImage.objects.filter(is_active=True).select_related('category')
    serializer_class = GalleryImageListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'event_type', 'is_featured']
    search_fields = ['title', 'description', 'event_type', 'location']
    ordering_fields = ['created_at', 'views_count', 'event_date']
    ordering = ['-is_featured', '-created_at']


class GalleryImageDetailView(generics.RetrieveAPIView):
    """Детальная информация об изображении"""
    queryset = GalleryImage.objects.filter(is_active=True).select_related('category')
    serializer_class = GalleryImageSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Увеличиваем счетчик просмотров
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedGalleryView(generics.ListAPIView):
    """Рекомендуемые изображения"""
    queryset = GalleryImage.objects.filter(is_active=True, is_featured=True).select_related('category')
    serializer_class = GalleryImageListSerializer


class GalleryByCategoryView(generics.ListAPIView):
    """Изображения по категории"""
    serializer_class = GalleryImageListSerializer
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return GalleryImage.objects.filter(
            is_active=True,
            category__slug=category_slug,
            category__is_active=True
        ).select_related('category')


class ClientReviewListView(generics.ListAPIView):
    """Список отзывов клиентов"""
    queryset = ClientReview.objects.filter(is_approved=True).select_related('gallery_image')
    serializer_class = ClientReviewSerializer
    ordering = ['-is_featured', '-created_at']


class ClientReviewCreateView(generics.CreateAPIView):
    """Создание отзыва клиента"""
    queryset = ClientReview.objects.all()
    serializer_class = ClientReviewCreateSerializer


class FeaturedReviewsView(generics.ListAPIView):
    """Рекомендуемые отзывы"""
    queryset = ClientReview.objects.filter(is_approved=True, is_featured=True).select_related('gallery_image')
    serializer_class = ClientReviewSerializer

