from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Color, Source, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'color_preview', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'hex_code']
    list_editable = ['is_active']

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.hex_code
        )
    color_preview.short_description = 'Предпросмотр'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'url']
    list_editable = ['is_active']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['created_at']
        return []


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['name', 'email', 'rating', 'comment', 'created_at']
    fields = ['name', 'rating', 'comment', 'is_approved', 'created_at']
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'shape', 'theme', 'base_price', 
        'discount_price', 'is_featured', 'is_active', 'views_count'
    ]
    list_filter = [
        'category', 'shape', 'theme', 'is_featured', 'is_active', 
        'is_customizable', 'custom_text_available', 'created_at'
    ]
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']
    filter_horizontal = ['colors', 'sources']
    inlines = [ProductImageInline, ReviewInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Характеристики', {
            'fields': ('shape', 'theme', 'colors', 'sources')
        }),
        ('Цены и количество', {
            'fields': ('base_price', 'discount_price', 'min_quantity', 'max_quantity')
        }),
        ('Кастомизация', {
            'fields': ('is_customizable', 'custom_text_available')
        }),
        ('Настройки', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['views_count']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_main', 'order']
    list_filter = ['is_main', 'product__category']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_main', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at', 'product__category']
    search_fields = ['name', 'email', 'comment', 'product__name']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'email')
        }),
        ('Отзыв', {
            'fields': ('product', 'rating', 'comment')
        }),
        ('Модерация', {
            'fields': ('is_approved', 'created_at')
        })
    )

