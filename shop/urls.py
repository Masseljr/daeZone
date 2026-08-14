from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product pages
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
    path('orders/', views.orders_view, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
