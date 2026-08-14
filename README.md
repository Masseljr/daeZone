# DaeZone E-Commerce Platform

A modern, full-featured e-commerce website built with Django, featuring a clean design with Deep Navy, Light Gray, and Warm Amber color scheme.

## 🎨 Design

- **Primary Color**: Deep Navy (#1a2332) - Headers, buttons, text
- **Secondary Color**: Light Gray (#f5f5f5) - Backgrounds, cards
- **Accent Color**: Warm Amber (#ffbf00) - CTAs, hover effects, SALE badges

## ✨ Features

### Customer Features
- 🛍️ Product browsing with category filtering
- 🔍 Search functionality
- 💰 Product discounts with SALE badges
- 🛒 Shopping cart (guest & authenticated users)
- 👤 User registration and authentication
- 📦 Order placement and tracking
- 💳 Multiple payment methods (simulated)
- 📍 Shipping address management
- 📊 Order history with status tracking

### Admin Features
- ➕ Add/Edit/Delete products
- 💸 Set discounts (0-100%) on products
- 📦 Manage orders and update status
- 🚚 Set custom delivery dates for orders
- 📈 Stock management
- 👥 User management
- 🎯 Bulk discount actions

### Order Status Automation (Semi-Automatic)
1. **Pending** → **Processing** (auto after 30 seconds)
2. **Processing** → **Shipped** (admin marks manually + sets delivery date)
3. **Shipped** → **Delivered** (auto on estimated delivery date)

## 📁 Project Structure

```
DaeZone/
├── manage.py
├── db.sqlite3 (gitignored)
├── README.md
├── requirements.txt
├── requirements-prod.txt
├── .env.example
├── .gitignore
│
├── media/ (gitignored)
│   └── products/
│
├── daezone/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── shop/
    ├── models.py (Category, Product, Cart, CartItem, Order, OrderItem, Payment, Address)
    ├── views.py (All business logic)
    ├── forms.py (Registration, Login, Checkout, Payment)
    ├── admin.py (Admin panel configuration)
    ├── urls.py
    ├── tasks.py (Background tasks)
    │
    ├── management/commands/
    │   └── run_scheduler.py
    │
    ├── static/shop/
    │   ├── css/style.css
    │   └── js/script.js
    │
    └── templates/shop/
        ├── base.html
        ├── home.html
        ├── product_detail.html
        ├── cart.html
        ├── checkout.html
        ├── login.html
        ├── register.html
        ├── orders.html
        ├── order_detail.html
        └── order_success.html
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2
- Pillow (image handling)
- APScheduler (background tasks)
- python-decouple (environment variables)

### Step 2: Environment Setup

Copy the example environment file:

```bash
copy .env.example .env
```

The default settings work for development. No changes needed unless deploying to production.

### Step 3: Database Setup

Run migrations to create the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

The site will be available at: **http://localhost:8000**

Admin panel at: **http://localhost:8000/admin**

### Step 6: Start Order Status Automation (Optional)

Open a **second terminal** and run:

```bash
python manage.py run_scheduler
```

This runs the background task that:
- Updates "Pending" → "Processing" after 30 seconds
- Updates "Shipped" → "Delivered" on the estimated delivery date

**Note**: This terminal must stay open for automation to work.

## 📝 How to Use

### For Admin:

1. **Login to Admin Panel**: http://localhost:8000/admin
2. **Add Categories**: Products → Categories → Add Category
3. **Add Products**:
   - Go to Products → Add Product
   - Fill in name, category, description, price
   - Upload image (optional)
   - Set stock quantity
   - Set discount percentage (0-100) for sales
4. **Manage Orders**:
   - View all orders in Orders section
   - Click an order to view details
   - Change status or set estimated delivery date
   - Use bulk actions to mark multiple orders as shipped

### For Customers:

1. **Browse Products**: Visit http://localhost:8000
2. **Register Account**: Click Register, fill form
3. **Add to Cart**: Click "Add to Cart" on products
4. **Checkout**: 
   - Go to Cart
   - Click "Proceed to Checkout"
   - Enter shipping address
   - Select payment method
   - Place order
5. **Track Orders**: Click "My Orders" to see order history

## 🎯 Admin Quick Actions

### Bulk Discount Products:
1. Go to Admin → Products
2. Select products (checkboxes)
3. Choose action: "Apply 10% discount" / "Apply 25% discount" / etc.
4. Click "Go"

### Mark Orders as Shipped:
1. Go to Admin → Orders
2. Select orders
3. Choose action: "Mark as Shipped (7-day delivery)" or "Mark as Shipped (next-day delivery)"
4. Click "Go"

### Custom Delivery Date:
1. Open an order in admin
2. Set "Status" to "Shipped"
3. Set "Estimated delivery date" to your chosen date
4. Save

## 🧪 Adding Sample Data

### Via Admin Panel:
1. Login to admin
2. Add 2-3 categories (Electronics, Clothing, Books, etc.)
3. Add 5-10 products with different prices and discounts
4. Upload product images or leave blank for placeholders

### Via Django Shell (Advanced):
```bash
python manage.py shell
```

```python
from shop.models import Category, Product
from decimal import Decimal

# Create category
cat = Category.objects.create(name="Electronics", description="Tech products")

# Create product
Product.objects.create(
    category=cat,
    name="Wireless Headphones",
    description="High-quality wireless headphones with noise cancellation",
    original_price=Decimal("99.99"),
    discount_percent=20,
    stock=50,
    is_active=True
)
```

## 🔧 Configuration

### Change Site Settings:
Edit `daezone/settings.py`:
- `SECRET_KEY`: Change for production
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain

### Change Automation Timings:
Edit `shop/tasks.py`:
- Line 16: Change `timedelta(seconds=30)` for Pending→Processing delay
- Line 34: Check `estimated_delivery_date__lte=now` for Shipped→Delivered

## 🌐 Production Deployment

### Use Production Requirements:
```bash
pip install -r requirements-prod.txt
```

This adds:
- Celery + Redis (production-grade task queue)
- Gunicorn (production server)
- psycopg2 (PostgreSQL support)

### Switch to Celery:
For production, replace APScheduler with Celery:

1. Install Redis
2. Configure Celery in `daezone/celery.py`
3. Run Celery worker: `celery -A daezone worker -l info`
4. Run Celery beat: `celery -A daezone beat -l info`

### Database:
Switch from SQLite to PostgreSQL:
- Update `DATABASES` in settings.py
- Run migrations

### Static/Media Files:
- Collect static files: `python manage.py collectstatic`
- Configure Nginx to serve media files
- Or use cloud storage (AWS S3, Cloudinary)

## 🛡️ Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use HTTPS in production
- Add CSRF trusted origins
- Use environment variables for sensitive data
- Never commit `.env` file to git

## 🐛 Troubleshooting

### Images not loading:
- Make sure `media/` folder exists
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Ensure DEBUG=True for development

### Cart count not updating:
- Check JavaScript console for errors
- Verify CSRF token is present
- Clear browser cache

### Scheduler not working:
- Ensure `run_scheduler` command is running in separate terminal
- Check for Python errors in scheduler terminal
- Verify orders exist in database

### Database errors:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📚 Technology Stack

- **Backend**: Django 4.2 (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Task Queue**: APScheduler (dev) / Celery + Redis (production)
- **Image Processing**: Pillow
- **Authentication**: Django built-in

## 🔐 Default Admin Credentials

After running `createsuperuser`, use those credentials.

**Never use default credentials in production!**

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Support

For issues or questions:
1. Check this README
2. Review Django documentation
3. Check browser console for JavaScript errors
4. Check terminal for Python errors

---

**Built with ❤️ for DaeZone**

*Modern E-Commerce Made Simple*
