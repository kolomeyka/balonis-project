from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Color, Source


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'color_preview', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'hex_code']

    def color_preview(self, obj):
        """Показывает превью цвета в админке"""
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.hex_code
        )

    color_preview.short_description = 'Превью'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'image_preview', 'base_price',
        'discount_price', 'is_active', 'is_featured', 'views_count'
    ]
    list_filter = [
        'category', 'colors', 'shape', 'theme',
        'is_active', 'is_featured', 'is_customizable', 'created_at'
    ]
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['colors', 'sources']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'image_preview_large']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview_large'),
            'description': 'Загрузите изображение товара для отображения в каталоге'
        }),
        ('Характеристики', {
            'fields': ('colors', 'sources', 'shape', 'theme')
        }),
        ('Цены и количество', {
            'fields': ('base_price', 'discount_price', 'min_quantity', 'max_quantity')
        }),
        ('Настройки', {
            'fields': ('is_customizable', 'custom_text_available', 'is_active', 'is_featured')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Маленькое превью изображения в списке"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = 'Изображение'

    def image_preview_large(self, obj):
        """Большое превью изображения в форме редактирования"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return "Изображение не загружено"

    image_preview_large.short_description = 'Превью изображения'

    def save_model(self, request, obj, form, change):
        """Автоматическое создание slug если не указан"""
        if not obj.slug:
            from django.utils.text import slugify
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

