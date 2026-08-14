"""
Background tasks for order status automation
Uses APScheduler for development/demo
"""
from django.utils import timezone
from datetime import timedelta
from .models import Order


def update_order_statuses():
    """
    Auto-update order statuses based on time elapsed
    - Pending → Processing (after 30 seconds)
    - Shipped → Delivered (on estimated delivery date)
    """
    now = timezone.now()
    
    # Update Pending to Processing (after 30 seconds)
    pending_cutoff = now - timedelta(seconds=30)
    pending_orders = Order.objects.filter(
        status='pending',
        created_at__lte=pending_cutoff
    )
    
    updated_count = 0
    for order in pending_orders:
        order.status = 'processing'
        order.save()
        updated_count += 1
        print(f"✓ Order {order.order_number} updated: Pending → Processing")
    
    # Update Shipped to Delivered (on or after estimated delivery date)
    shipped_orders = Order.objects.filter(
        status='shipped',
        estimated_delivery_date__lte=now
    )
    
    for order in shipped_orders:
        order.status = 'delivered'
        order.save()
        updated_count += 1
        print(f"✓ Order {order.order_number} updated: Shipped → Delivered")
    
    if updated_count > 0:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Updated {updated_count} order(s)")
    
    return updated_count
