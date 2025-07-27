from django.db import models


class GalleryCategory(models.Model):
    """Категории галереи"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Категория галереи"
        verbose_name_plural = "Категории галереи"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Изображения в галерее"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='gallery/', verbose_name="Изображение")
    category = models.ForeignKey(
        GalleryCategory, 
        related_name='images', 
        on_delete=models.CASCADE, 
        verbose_name="Категория"
    )
    
    # Метаданные
    event_type = models.CharField(max_length=100, blank=True, verbose_name="Тип мероприятия")
    location = models.CharField(max_length=200, blank=True, verbose_name="Место проведения")
    event_date = models.DateField(blank=True, null=True, verbose_name="Дата мероприятия")
    
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.title


class ClientReview(models.Model):
    """Отзывы клиентов"""
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    review_text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Оценка"
    )
    
    # Связь с изображением из галереи (опционально)
    gallery_image = models.ForeignKey(
        GalleryImage, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        verbose_name="Связанное изображение"
    )
    
    is_approved = models.BooleanField(default=False, verbose_name="Одобрен")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Отзыв клиента"
        verbose_name_plural = "Отзывы клиентов"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"Отзыв от {self.name} ({self.rating}/5)"

