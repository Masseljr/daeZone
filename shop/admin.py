from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Payment, Address


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'original_price', 'discount_percent', 'sale_price_display', 
                    'stock', 'is_active', 'sale_badge']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['discount_percent', 'stock', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('original_price', 'discount_percent'),
            'description': 'Set discount percentage (0-100) to apply sale pricing'
        }),
        ('Inventory', {
            'fields': ('stock', 'is_active')
        }),
    )

    def sale_price_display(self, obj):
        """Display calculated sale price"""
        return f"${obj.sale_price:.2f}"
    sale_price_display.short_description = 'Sale Price'

    def sale_badge(self, obj):
        """Display SALE badge if product is on sale"""
        if obj.is_on_sale:
            return format_html('<span style="background-color: #ffbf00; color: #1a2332; padding: 3px 8px; border-radius: 3px; font-weight: bold;">SALE</span>')
        return '-'
    sale_badge.short_description = 'Sale Status'

    actions = ['apply_10_discount', 'apply_25_discount', 'apply_50_discount', 'remove_discount']

    def apply_10_discount(self, request, queryset):
        queryset.update(discount_percent=10)
        self.message_user(request, f"{queryset.count()} products now have 10% discount")
    apply_10_discount.short_description = "Apply 10%% discount"

    def apply_25_discount(self, request, queryset):
        queryset.update(discount_percent=25)
        self.message_user(request, f"{queryset.count()} products now have 25% discount")
    apply_25_discount.short_description = "Apply 25%% discount"

    def apply_50_discount(self, request, queryset):
        queryset.update(discount_percent=50)
        self.message_user(request, f"{queryset.count()} products now have 50% discount")
    apply_50_discount.short_description = "Apply 50%% discount"

    def remove_discount(self, request, queryset):
        queryset.update(discount_percent=0)
        self.message_user(request, f"Removed discounts from {queryset.count()} products")
    remove_discount.short_description = "Remove discount"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'discount_applied', 'total_price']
    can_delete = False


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ['payment_method', 'amount', 'status', 'transaction_id', 'created_at']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status_badge', 'total_items', 
                    'created_at', 'estimated_delivery_date']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline, PaymentInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_amount', 'created_at', 'updated_at')
        }),
        ('Shipping', {
            'fields': ('shipping_address', 'status', 'shipped_at', 'estimated_delivery_date'),
            'description': 'When marking as "Shipped", set the estimated delivery date. Order will auto-mark as "Delivered" on that date.'
        }),
    )

    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'pending': '#6c757d',
            'processing': '#007bff',
            'shipped': '#ffbf00',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_as_shipped_7days', 'mark_as_shipped_next_day', 'mark_as_cancelled']

    def mark_as_shipped_7days(self, request, queryset):
        """Mark orders as shipped with 7-day delivery estimate"""
        now = timezone.now()
        delivery_date = now + timedelta(days=7)
        count = queryset.filter(status__in=['pending', 'processing']).update(
            status='shipped',
            shipped_at=now,
            estimated_delivery_date=delivery_date
        )
        self.message_user(request, f"{count} orders marked as shipped (delivery in 7 days)")
    mark_as_shipped_7days.short_description = "Mark as Shipped (7-day delivery)"

    def mark_as_shipped_next_day(self, request, queryset):
        """Mark orders as shipped with next-day delivery"""
        now = timezone.now()
        delivery_date = now + timedelta(days=1)
        count = queryset.filter(status__in=['pending', 'processing']).update(
            status='shipped',
            shipped_at=now,
            estimated_delivery_date=delivery_date
        )
        self.message_user(request, f"{count} orders marked as shipped (next-day delivery)")
    mark_as_shipped_next_day.short_description = "Mark as Shipped (next-day delivery)"

    def mark_as_cancelled(self, request, queryset):
        """Cancel orders"""
        count = queryset.exclude(status__in=['delivered', 'cancelled']).update(status='cancelled')
        self.message_user(request, f"{count} orders cancelled")
    mark_as_cancelled.short_description = "Cancel orders"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order__order_number', 'transaction_id']
    readonly_fields = ['created_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'postal_code', 'is_default']
    list_filter = ['is_default', 'country', 'state']
    search_fields = ['full_name', 'user__username', 'city', 'postal_code']
