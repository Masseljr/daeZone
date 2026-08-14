"""
Django management command to load sample products
Usage: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from shop.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample categories and products for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest tech gadgets and devices'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  ✓ Created category: {cat.name}')
            else:
                self.stdout.write(f'  - Category exists: {cat.name}')
        
        # Create products
        products_data = [
            {
                'category': 'Electronics',
                'name': 'Wireless Bluetooth Headphones',
                'description': 'Premium noise-cancelling headphones with 30-hour battery life. Perfect for music lovers and professionals.',
                'original_price': Decimal('129.99'),
                'discount_percent': 25,
                'stock': 45,
            },
            {
                'category': 'Electronics',
                'name': 'Smart Watch Pro',
                'description': 'Track your fitness goals with this advanced smartwatch featuring heart rate monitoring and GPS.',
                'original_price': Decimal('299.99'),
                'discount_percent': 15,
                'stock': 30,
            },
            {
                'category': 'Electronics',
                'name': 'USB-C Fast Charger',
                'description': 'Charge your devices quickly with this 65W USB-C charger compatible with laptops, tablets, and phones.',
                'original_price': Decimal('39.99'),
                'discount_percent': 0,
                'stock': 100,
            },
            {
                'category': 'Clothing',
                'name': 'Classic Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors. Perfect for everyday wear.',
                'original_price': Decimal('24.99'),
                'discount_percent': 20,
                'stock': 200,
            },
            {
                'category': 'Clothing',
                'name': 'Slim Fit Jeans',
                'description': 'Premium denim jeans with a modern slim fit. Durable and stylish for any occasion.',
                'original_price': Decimal('79.99'),
                'discount_percent': 30,
                'stock': 75,
            },
            {
                'category': 'Clothing',
                'name': 'Winter Jacket',
                'description': 'Stay warm this winter with our insulated jacket featuring water-resistant material.',
                'original_price': Decimal('149.99'),
                'discount_percent': 40,
                'stock': 35,
            },
            {
                'category': 'Books',
                'name': 'The Art of Programming',
                'description': 'Comprehensive guide to modern programming practices. Perfect for beginners and experts alike.',
                'original_price': Decimal('49.99'),
                'discount_percent': 10,
                'stock': 60,
            },
            {
                'category': 'Books',
                'name': 'Mystery Novel Collection',
                'description': 'A thrilling collection of mystery novels from bestselling authors.',
                'original_price': Decimal('34.99'),
                'discount_percent': 0,
                'stock': 40,
            },
            {
                'category': 'Home & Garden',
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with multiple brightness levels. Perfect for reading and working.',
                'original_price': Decimal('45.99'),
                'discount_percent': 15,
                'stock': 80,
            },
            {
                'category': 'Home & Garden',
                'name': 'Indoor Plant Set',
                'description': 'Beautiful set of 3 low-maintenance indoor plants perfect for home or office.',
                'original_price': Decimal('59.99'),
                'discount_percent': 25,
                'stock': 50,
            },
        ]
        
        created_count = 0
        for prod_data in products_data:
            category = categories[prod_data['category']]
            prod, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'description': prod_data['description'],
                    'original_price': prod_data['original_price'],
                    'discount_percent': prod_data['discount_percent'],
                    'stock': prod_data['stock'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                sale_badge = f" (SALE {prod.discount_percent}% OFF)" if prod.is_on_sale else ""
                self.stdout.write(f'  ✓ Created product: {prod.name}{sale_badge} - ${prod.sale_price}')
            else:
                self.stdout.write(f'  - Product exists: {prod.name}')
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✓ Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(categories)} categories'))
        self.stdout.write(self.style.SUCCESS(f'  - {created_count} new products created'))
        self.stdout.write('')
        self.stdout.write('Visit http://localhost:8000 to see the products!')
