from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Категории шариковых композиций"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Color(models.Model):
    """Цвета шариков"""
    name = models.CharField(max_length=50, verbose_name="Название")
    hex_code = models.CharField(max_length=7, verbose_name="HEX код", help_text="Например: #FF0000")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        ordering = ['name']

    def __str__(self):
        return self.name


class Source(models.Model):
    """Источники для покупки материалов"""
    name = models.CharField(max_length=100, verbose_name="Название источника")
    url = models.URLField(verbose_name="URL для покупки")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Источник материалов"
        verbose_name_plural = "Источники материалов"
        ordering = ['name']

    def __str__(self):
        return self.name

# class Review(models.Model):
#     """Отзывы о товарах"""
#     product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="Товар")
#     name = models.CharField(max_length=100, verbose_name="Имя")
#     email = models.EmailField(verbose_name="Email")
#     rating = models.PositiveIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(5)],
#         verbose_name="Оценка"
#     )
#     comment = models.TextField(verbose_name="Комментарий")
#     is_approved = models.BooleanField(default=False, verbose_name="Одобрен")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
#     verbose_name = "Отзыв"
#     verbose_name_plural = "Отзывы"
#     ordering = ['-created_at']
#     def __str__(self):
#         return f"Отзыв от {self.name} на {self.product.name}"


class Product(models.Model):
    """Товары - шариковые композиции"""
    SHAPE_CHOICES = [
        ('round', 'Круглые'),
        ('heart', 'Сердечки'),
        ('star', 'Звезды'),
        ('number', 'Цифры'),
        ('letter', 'Буквы'),
        ('foil', 'Фольгированные'),
        ('latex', 'Латексные'),
    ]

    THEME_CHOICES = [
        ('wedding', 'Свадьба'),
        ('corporate', 'Корпоратив'),
        ('graduation', 'Выпускной'),
        ('anniversary', 'Годовщина'),
        ('baby_shower', 'Рождение ребенка'),
        ('valentine', 'День святого Валентина'),
        ('new_year', 'Новый год'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")

    # ДОБАВЛЕНО: Поле для изображения
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Изображение товара",
        help_text="Загрузите основное изображение товара"
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    colors = models.ManyToManyField(Color, verbose_name="Доступные цвета")
    sources = models.ManyToManyField(Source, blank=True, verbose_name="Источники материалов")

    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, verbose_name="Форма")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, verbose_name="Тематика")

    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name="Цена со скидкой")

    min_quantity = models.PositiveIntegerField(default=1, verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(default=100, verbose_name="Максимальное количество")

    is_customizable = models.BooleanField(default=True, verbose_name="Можно кастомизировать")
    custom_text_available = models.BooleanField(default=False, verbose_name="Доступна надпись")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")

    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Возвращает финальную цену (со скидкой если есть)"""
        return self.discount_price if self.discount_price else self.base_price

    @property
    def has_discount(self):
        """Проверяет есть ли скидка"""
        return self.discount_price is not None and self.discount_price < self.base_price
