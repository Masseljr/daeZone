from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
import uuid

from .models import Product, Category, Cart, CartItem, Order, OrderItem, Payment, Address
from .forms import (
    UserRegistrationForm, UserLoginForm, CheckoutForm, 
    PaymentForm, AddToCartForm
)


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_count_context(request):
    """Context processor for cart count"""
    cart = get_or_create_cart(request)
    return {'cart_count': cart.total_items}


# Product Views
def home(request):
    """Home page with product listings"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = AddToCartForm()
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'shop/product_detail.html', context)


# Cart Views
def cart_view(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'shop/cart.html', context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if not product.in_stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Product out of stock'})
        messages.error(request, 'Product is out of stock')
        return redirect('shop:product_detail', slug=product.slug)
    
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Check stock
    if cart_item.quantity > product.stock:
        cart_item.quantity = product.stock
        cart_item.save()
        message = f'Only {product.stock} items available'
    else:
        message = 'Product added to cart'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items
        })
    
    messages.success(request, message)
    return redirect('shop:cart')


def update_cart(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        if quantity > cart_item.product.stock:
            messages.warning(request, f'Only {cart_item.product.stock} items available')
            cart_item.quantity = cart_item.product.stock
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    
    return redirect('shop:cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    messages.success(request, 'Item removed from cart')
    return redirect('shop:cart')


# Authentication Views
def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Transfer guest cart to user
            if request.session.session_key:
                try:
                    guest_cart = Cart.objects.get(session_key=request.session.session_key)
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    
                    # Transfer items
                    for item in guest_cart.items.all():
                        user_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={'quantity': item.quantity}
                        )
                        if not created:
                            user_item.quantity += item.quantity
                            user_item.save()
                    
                    guest_cart.delete()
                except Cart.DoesNotExist:
                    pass
            
            messages.success(request, f'Welcome to DaeZone, {user.username}!')
            return redirect('shop:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Transfer guest cart to user
            if request.session.session_key:
                try:
                    guest_cart = Cart.objects.get(session_key=request.session.session_key)
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    
                    for item in guest_cart.items.all():
                        user_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={'quantity': item.quantity}
                        )
                        if not created:
                            user_item.quantity += item.quantity
                            user_item.save()
                    
                    guest_cart.delete()
                except Cart.DoesNotExist:
                    pass
            
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'shop:home')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('shop:home')


# Checkout Views
@login_required
def checkout_view(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty')
        return redirect('shop:cart')
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} has insufficient stock')
            return redirect('shop:cart')
    
    # Get user's default address or create new
    default_address = Address.objects.filter(user=request.user, is_default=True).first()
    
    if request.method == 'POST':
        address_form = CheckoutForm(request.POST, instance=default_address)
        payment_form = PaymentForm(request.POST)
        
        if address_form.is_valid() and payment_form.is_valid():
            # Save address
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                total_amount=cart.subtotal,
                status='pending'
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.sale_price,
                    discount_applied=item.product.original_price - item.product.sale_price
                )
                
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()
            
            # Create payment
            payment_method = payment_form.cleaned_data['payment_method']
            Payment.objects.create(
                order=order,
                payment_method=payment_method,
                amount=order.total_amount,
                status='completed',
                transaction_id=f'TXN{uuid.uuid4().hex[:12].upper()}'
            )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order placed successfully! Order #{order.order_number}')
            return redirect('shop:order_success', order_id=order.id)
    else:
        address_form = CheckoutForm(instance=default_address)
        payment_form = PaymentForm()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'address_form': address_form,
        'payment_form': payment_form,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_success(request, order_id):
    """Order success confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


@login_required
def orders_view(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/orders.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_detail.html', context)
