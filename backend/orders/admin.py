from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'selected_color', 'quantity', 'price', 'total_price']
    fields = ['product', 'selected_color', 'custom_text', 'quantity', 'price', 'total_price', 'notes']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'customer_phone', 'status', 
        'delivery_date', 'total_with_delivery', 'created_at'
    ]
    list_filter = [
        'status', 'payment_method', 'delivery_date', 'created_at'
    ]
    search_fields = [
        'customer_name', 'customer_phone', 'customer_email', 
        'delivery_address', 'id'
    ]
    list_editable = ['status']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'delivery_date', 'delivery_time')
        }),
        ('Заказ', {
            'fields': ('status', 'payment_method', 'total_amount', 'delivery_cost', 'total_with_delivery')
        }),
        ('Комментарии', {
            'fields': ('notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['total_with_delivery', 'created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

    def total_with_delivery(self, obj):
        return f"{obj.total_with_delivery}₽"
    total_with_delivery.short_description = 'Итого с доставкой'

    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_completed']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} заказов отмечено как подтвержденные.')
    mark_as_confirmed.short_description = 'Отметить как подтвержденные'

    def mark_as_preparing(self, request, queryset):
        updated = queryset.update(status='preparing')
        self.message_user(request, f'{updated} заказов отмечено как готовящиеся.')
    mark_as_preparing.short_description = 'Отметить как готовящиеся'

    def mark_as_ready(self, request, queryset):
        updated = queryset.update(status='ready')
        self.message_user(request, f'{updated} заказов отмечено как готовые к доставке.')
    mark_as_ready.short_description = 'Отметить как готовые к доставке'

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} заказов отмечено как выполненные.')
    mark_as_completed.short_description = 'Отметить как выполненные'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order_link', 'product', 'selected_color',
        'quantity', 'price', 'total_price'
    ]
    list_filter = [
        'product__category', 'selected_color',
        'order__status', 'order__created_at'
    ]
    search_fields = [
        'product__name', 'order__customer_name', 'custom_text'
    ]
    readonly_fields = ['total_price']

    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order)
    order_link.short_description = 'Заказ'
    order_link.admin_order_field = 'order'

    def total_price(self, obj):
        return f"{obj.total_price}₽"
    total_price.short_description = 'Итого'


