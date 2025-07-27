from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage, ClientReview


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'images_count', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']

    def images_count(self, obj):
        return obj.images.filter(is_active=True).count()
    images_count.short_description = 'Количество изображений'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'image_preview', 'category', 'event_type', 
        'is_featured', 'is_active', 'views_count', 'created_at'
    ]
    list_filter = [
        'category', 'event_type', 'is_featured', 'is_active', 
        'event_date', 'created_at'
    ]
    search_fields = ['title', 'description', 'event_type', 'location']
    list_editable = ['is_featured', 'is_active']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Метаданные события', {
            'fields': ('event_type', 'location', 'event_date')
        }),
        ('Настройки', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['views_count']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    actions = ['mark_as_featured', 'unmark_as_featured', 'activate', 'deactivate']

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} изображений отмечено как рекомендуемые.')
    mark_as_featured.short_description = 'Отметить как рекомендуемые'

    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} изображений убрано из рекомендуемых.')
    unmark_as_featured.short_description = 'Убрать из рекомендуемых'

    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} изображений активировано.')
    activate.short_description = 'Активировать'

    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} изображений деактивировано.')
    deactivate.short_description = 'Деактивировать'


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'rating_stars', 'gallery_image_link', 
        'is_featured', 'is_approved', 'created_at'
    ]
    list_filter = [
        'rating', 'is_featured', 'is_approved', 'created_at'
    ]
    search_fields = ['name', 'email', 'review_text']
    list_editable = ['is_featured', 'is_approved']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Отзыв', {
            'fields': ('review_text', 'rating', 'gallery_image')
        }),
        ('Модерация', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at']

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 16px;">{}</span>',
            stars
        )
    rating_stars.short_description = 'Рейтинг'

    def gallery_image_link(self, obj):
        if obj.gallery_image:
            return format_html(
                '<a href="/admin/gallery/galleryimage/{}/change/">{}</a>',
                obj.gallery_image.id,
                obj.gallery_image.title
            )
        return "Не связано"
    gallery_image_link.short_description = 'Связанное изображение'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('gallery_image')

    actions = ['approve_reviews', 'disapprove_reviews', 'mark_as_featured', 'unmark_as_featured']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} отзывов одобрено.')
    approve_reviews.short_description = 'Одобрить отзывы'

    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} отзывов отклонено.')
    disapprove_reviews.short_description = 'Отклонить отзывы'

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} отзывов отмечено как рекомендуемые.')
    mark_as_featured.short_description = 'Отметить как рекомендуемые'

    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} отзывов убрано из рекомендуемых.')
    unmark_as_featured.short_description = 'Убрать из рекомендуемых'

