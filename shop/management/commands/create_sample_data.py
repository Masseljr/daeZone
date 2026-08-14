"""
Django management command to create sample products and categories
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Create sample categories and products for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data for DaeZone...'))
        
        # Create Categories
        electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            defaults={'description': "Latest electronic devices and gadgets"}
        )
        
        clothing, _ = Category.objects.get_or_create(
            name="Clothing",
            defaults={'description': "Fashion and apparel for everyone"}
        )
        
        home, _ = Category.objects.get_or_create(
            name="Home & Garden",
            defaults={'description': "Home decor and garden essentials"}
        )
        
        sports, _ = Category.objects.get_or_create(
            name="Sports & Outdoors",
            defaults={'description': "Sports equipment and outdoor gear"}
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {Category.objects.count()} categories'))
        
        # Create Sample Products
        products_data = [
            # Electronics
            {
                'category': electronics,
                'name': 'Wireless Bluetooth Headphones',
                'description': 'Premium noise-canceling wireless headphones with 30-hour battery life. Crystal clear sound quality and comfortable design for all-day wear.',
                'original_price': 149.99,
                'discount_percent': 25,
                'stock': 50
            },
            {
                'category': electronics,
                'name': 'Smartphone Pro Max',
                'description': 'Latest flagship smartphone with advanced camera system, 5G connectivity, and stunning OLED display. 256GB storage.',
                'original_price': 999.99,
                'discount_percent': 10,
                'stock': 30
            },
            {
                'category': electronics,
                'name': 'Laptop Ultra Slim',
                'description': '13-inch ultraportable laptop with Intel i7 processor, 16GB RAM, 512GB SSD. Perfect for work and entertainment.',
                'original_price': 1299.99,
                'discount_percent': 15,
                'stock': 20
            },
            {
                'category': electronics,
                'name': 'Smart Watch Fitness Tracker',
                'description': 'Track your fitness goals with this advanced smartwatch. Heart rate monitor, GPS, sleep tracking, and 7-day battery life.',
                'original_price': 249.99,
                'discount_percent': 0,
                'stock': 75
            },
            
            # Clothing
            {
                'category': clothing,
                'name': 'Classic Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt in various colors. Perfect for casual wear. Available in S, M, L, XL.',
                'original_price': 24.99,
                'discount_percent': 20,
                'stock': 200
            },
            {
                'category': clothing,
                'name': 'Denim Jeans Slim Fit',
                'description': 'Modern slim-fit jeans with stretch fabric for comfort. Classic 5-pocket design. Premium denim quality.',
                'original_price': 79.99,
                'discount_percent': 30,
                'stock': 100
            },
            {
                'category': clothing,
                'name': 'Winter Jacket Waterproof',
                'description': 'Stay warm and dry with this insulated waterproof jacket. Multiple pockets and adjustable hood.',
                'original_price': 189.99,
                'discount_percent': 35,
                'stock': 45
            },
            {
                'category': clothing,
                'name': 'Running Shoes Athletic',
                'description': 'Lightweight running shoes with superior cushioning and breathable mesh upper. Ideal for daily training.',
                'original_price': 119.99,
                'discount_percent': 0,
                'stock': 80
            },
            
            # Home & Garden
            {
                'category': home,
                'name': 'Coffee Maker Automatic',
                'description': 'Programmable coffee maker with 12-cup capacity. Auto-brew feature and pause-and-serve function.',
                'original_price': 89.99,
                'discount_percent': 15,
                'stock': 60
            },
            {
                'category': home,
                'name': 'Bed Sheets Premium Cotton',
                'description': 'Luxury 400-thread count Egyptian cotton bed sheets. Soft, breathable, and durable. Queen size.',
                'original_price': 129.99,
                'discount_percent': 25,
                'stock': 40
            },
            {
                'category': home,
                'name': 'Indoor Plant Collection',
                'description': 'Set of 3 low-maintenance indoor plants. Includes decorative pots. Perfect for home or office.',
                'original_price': 49.99,
                'discount_percent': 10,
                'stock': 35
            },
            
            # Sports & Outdoors
            {
                'category': sports,
                'name': 'Yoga Mat Premium',
                'description': 'Extra thick non-slip yoga mat with carrying strap. Eco-friendly material. Perfect for yoga, pilates, and stretching.',
                'original_price': 39.99,
                'discount_percent': 20,
                'stock': 90
            },
            {
                'category': sports,
                'name': 'Camping Tent 4-Person',
                'description': 'Spacious 4-person tent with easy setup. Waterproof and wind-resistant. Great for camping and outdoor adventures.',
                'original_price': 199.99,
                'discount_percent': 40,
                'stock': 25
            },
            {
                'category': sports,
                'name': 'Dumbbell Set Adjustable',
                'description': 'Adjustable dumbbell set from 5-52 lbs. Space-saving design. Perfect for home gym workouts.',
                'original_price': 299.99,
                'discount_percent': 0,
                'stock': 30
            },
            {
                'category': sports,
                'name': 'Basketball Official Size',
                'description': 'Official size and weight basketball with superior grip. Indoor and outdoor use. Durable rubber construction.',
                'original_price': 29.99,
                'discount_percent': 15,
                'stock': 100
            },
        ]
        
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} new products'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total products in database: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data creation complete!'))
        self.stdout.write(self.style.WARNING('Note: Product images not included. Add via admin panel.'))
