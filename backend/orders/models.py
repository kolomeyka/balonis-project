from django.db import models
from django.core.validators import RegexValidator
from products.models import Product, Color


class Order(models.Model):
    """Заказы"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('confirmed', 'Подтвержден'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов к доставке'),
        ('delivering', 'Доставляется'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой'),
        ('online', 'Онлайн оплата'),
    ]

    # Информация о клиенте
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона")],
        verbose_name="Телефон"
    )
    customer_email = models.EmailField(blank=True, verbose_name="Email")

    # Адрес доставки
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(blank=True, null=True, verbose_name="Время доставки")
    
    # Детали заказа
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="Способ оплаты")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость доставки")
    
    notes = models.TextField(blank=True, verbose_name="Комментарии к заказу")
    admin_notes = models.TextField(blank=True, verbose_name="Заметки администратора")
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"

    @property
    def total_with_delivery(self):
        """Общая сумма с доставкой"""
        return self.total_amount + self.delivery_cost


class OrderItem(models.Model):
    """Позиции заказа"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    
    # Кастомизация
    selected_color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Выбранный цвет")
    custom_text = models.CharField(max_length=200, blank=True, verbose_name="Надпись")
    
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    
    notes = models.TextField(blank=True, verbose_name="Особые пожелания")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.price * self.quantity


class DeliveryZone(models.Model):
    """Зоны доставки"""
    name = models.CharField(max_length=100, verbose_name="Название зоны")
    description = models.TextField(blank=True, verbose_name="Описание")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость доставки")
    min_order_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Минимальная сумма заказа"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Зона доставки"
        verbose_name_plural = "Зоны доставки"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.delivery_cost}₽"

