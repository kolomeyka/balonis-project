from rest_framework import serializers
from .models import GalleryCategory, GalleryImage, ClientReview


class GalleryCategorySerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'images_count']
    
    def get_images_count(self, obj):
        return obj.images.filter(is_active=True).count()


class GalleryImageSerializer(serializers.ModelSerializer):
    category = GalleryCategorySerializer(read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'description', 'image', 'category',
            'event_type', 'location', 'event_date', 'is_featured',
            'views_count', 'created_at'
        ]


class GalleryImageListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка изображений"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'image', 'category_name', 'event_type',
            'is_featured', 'views_count', 'created_at'
        ]


class ClientReviewSerializer(serializers.ModelSerializer):
    gallery_image = GalleryImageListSerializer(read_only=True)
    
    class Meta:
        model = ClientReview
        fields = [
            'id', 'name', 'review_text', 'rating', 'gallery_image',
            'is_featured', 'created_at'
        ]


class ClientReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientReview
        fields = ['name', 'email', 'phone', 'review_text', 'rating', 'gallery_image']

