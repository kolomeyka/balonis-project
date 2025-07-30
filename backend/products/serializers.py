from rest_framework import serializers
from .models import Product, Category, Color, Source


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'description']


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров (краткая информация)"""
    category = CategorySerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    # ДОБАВЛЕНО: Поле image для отображения изображений
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'image',
            'category', 'colors', 'shape', 'theme',
            'base_price', 'discount_price', 'final_price', 'has_discount',
            'is_featured', 'views_count'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о товаре"""
    category = CategorySerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sources = SourceSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    has_discount = serializers.ReadOnlyField()
    # ДОБАВЛЕНО: Поле image для детального просмотра
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 'image',
            'category', 'colors', 'sources', 'shape', 'theme',
            'base_price', 'discount_price', 'final_price', 'has_discount',
            'min_quantity', 'max_quantity',
            'is_customizable', 'custom_text_available',
            'is_featured', 'views_count', 'created_at', 'updated_at'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания товара"""
    # ДОБАВЛЕНО: Поле image для загрузки изображений
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'short_description', 'image',
            'category', 'colors', 'sources', 'shape', 'theme',
            'base_price', 'discount_price',
            'min_quantity', 'max_quantity',
            'is_customizable', 'custom_text_available',
            'is_active', 'is_featured'
        ]

    def validate_slug(self, value):
        """Проверка уникальности slug"""
        if Product.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Товар с таким URL уже существует")
        return value

    def validate(self, data):
        """Общая валидация данных"""
        if data.get('discount_price') and data.get('base_price'):
            if data['discount_price'] >= data['base_price']:
                raise serializers.ValidationError(
                    "Цена со скидкой должна быть меньше базовой цены"
                )

        if data.get('min_quantity', 0) > data.get('max_quantity', 0):
            raise serializers.ValidationError(
                "Минимальное количество не может быть больше максимального"
            )

        return data

