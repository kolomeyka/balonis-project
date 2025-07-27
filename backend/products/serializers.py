from rest_framework import serializers
from .models import Category, Color, Source, Product, ProductImage, Review


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'rating', 'comment', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""
    category = CategorySerializer(read_only=True)
    main_image = serializers.SerializerMethodField()
    current_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'category',
            'shape', 'theme', 'base_price', 'discount_price', 
            'current_price', 'has_discount', 'is_featured',
            'main_image', 'views_count'
        ]
    
    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return ProductImageSerializer(main_image).data
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор товара"""
    category = CategorySerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sources = SourceSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    current_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'colors', 'sources', 'shape', 'theme',
            'base_price', 'discount_price', 'current_price', 'has_discount',
            'min_quantity', 'max_quantity', 'is_customizable', 
            'custom_text_available', 'is_featured', 'images', 
            'reviews', 'views_count', 'created_at'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания товара"""
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'short_description',
            'category', 'colors', 'sources', 'shape', 'theme',
            'base_price', 'discount_price', 'min_quantity', 
            'max_quantity', 'is_customizable', 'custom_text_available',
            'is_featured', 'is_active'
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""
    class Meta:
        model = Review
        fields = ['product', 'name', 'email', 'rating', 'comment']

