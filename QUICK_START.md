# 🚀 DaeZone Quick Start Guide

## ✅ Setup Complete!

Your DaeZone e-commerce site is now running with sample data.

---

## 🌐 Access Your Site

### Customer Site
**URL:** http://127.0.0.1:8000/

Browse products, add to cart, register, and place orders.

### Admin Panel
**URL:** http://127.0.0.1:8000/admin

**Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change this password in production!

---

## 📊 What's Already Set Up

✅ **Database:** SQLite with all tables created  
✅ **Sample Data:** 15 products across 4 categories  
✅ **Admin User:** Ready to manage products and orders  
✅ **Web Server:** Running on http://127.0.0.1:8000/  
✅ **Scheduler:** Background task automation running  

---

## 🎯 Sample Products Available

### Electronics (4 products)
- Wireless Bluetooth Headphones - **25% OFF**
- Smartphone Pro Max - **10% OFF**
- Laptop Ultra Slim - **15% OFF**
- Smart Watch Fitness Tracker

### Clothing (4 products)
- Classic Cotton T-Shirt - **20% OFF**
- Denim Jeans Slim Fit - **30% OFF**
- Winter Jacket Waterproof - **35% OFF**
- Running Shoes Athletic

### Home & Garden (3 products)
- Coffee Maker Automatic - **15% OFF**
- Bed Sheets Premium Cotton - **25% OFF**
- Indoor Plant Collection - **10% OFF**

### Sports & Outdoors (4 products)
- Yoga Mat Premium - **20% OFF**
- Camping Tent 4-Person - **40% OFF**
- Dumbbell Set Adjustable
- Basketball Official Size - **15% OFF**

---

## 🛍️ Try It Out!

### As a Customer:
1. Visit http://127.0.0.1:8000/
2. Browse products (notice the SALE badges!)
3. Click on a product to see details
4. Add items to cart (works without login!)
5. Click "Register" to create an account
6. Complete checkout with shipping address
7. View your orders in "My Orders"
8. Watch order status change automatically!

### As an Admin:
1. Visit http://127.0.0.1:8000/admin
2. Login with `admin` / `admin123`
3. Try these actions:
   - **Add a new product** with discount
   - **Edit product** prices and stock
   - **Apply bulk discounts** (select multiple products, choose action)
   - **View orders** and mark as shipped
   - **Set delivery dates** when shipping orders
   - **Manage categories** and organize products

---

## 🔄 Order Status Flow (Watch It Work!)

Place a test order and watch the magic:

1. **Place Order** → Status: **Pending** (instant)
2. **Wait 30 seconds** → Status: **Processing** (automatic!)
3. **Admin marks as Shipped** → Status: **Shipped** (manual, with delivery date)
4. **On delivery date** → Status: **Delivered** (automatic!)

The scheduler checks every minute, so you'll see changes quickly!

---

## 🎨 Color Scheme Reference

- **Deep Navy:** `#1a2332` - Navigation, headers, buttons
- **Light Gray:** `#f5f5f5` - Backgrounds
- **Warm Amber:** `#ffbf00` - Accents, sale badges, CTAs

---

## 📝 Common Admin Tasks

### Add New Product:
1. Go to **Products** → **Add Product**
2. Select category
3. Enter name, description
4. Set original price
5. Set discount (0-100%)
6. Add stock quantity
7. Upload image (optional)
8. Save!

### Apply Discounts:
1. Go to **Products**
2. Select multiple products (checkboxes)
3. Choose action: "Apply 10% discount" (or 25%, 50%)
4. Click "Go"

### Ship an Order:
1. Go to **Orders**
2. Click on an order
3. Change status to "Shipped"
4. Set "Shipped at" (defaults to now)
5. Set "Estimated delivery date" (when it should arrive)
6. Save
7. Order will auto-mark as "Delivered" on that date!

### Bulk Ship Orders:
1. Select multiple orders
2. Choose action: "Mark as Shipped (7-day delivery)"
3. Click "Go"
4. All orders shipped with 7-day delivery estimate!

---

## 🖼️ Adding Product Images

Product images make the site look better! Here's how:

1. Go to admin panel
2. Edit a product
3. Click "Choose File" under Image
4. Select an image from your computer
5. Save

**Image Tips:**
- Use square images (works best)
- Recommended size: 600x600px
- Formats: JPG, PNG
- Images saved to `media/products/YYYY/MM/DD/`

---

## 🛑 Stopping the Servers

When done testing:

1. **Stop Web Server:** Press `Ctrl+C` in the terminal running `runserver`
2. **Stop Scheduler:** Press `Ctrl+C` in the terminal running `run_scheduler`

To restart later:
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
python manage.py run_scheduler
```

---

## 🧪 Test Scenarios

### Scenario 1: Guest Shopping
1. Browse products without logging in
2. Add items to cart (cart counter updates)
3. Register for account
4. Cart automatically transfers!
5. Complete checkout

### Scenario 2: Discount Testing
1. Login to admin
2. Select 3-4 products
3. Apply 50% discount (bulk action)
4. Visit homepage as customer
5. See SALE badges and discounted prices!

### Scenario 3: Order Automation
1. Place an order as customer
2. Watch it change to "Processing" (~30 seconds)
3. Login to admin
4. Mark order as "Shipped" with tomorrow's date
5. Check order next day - it's "Delivered"!

---

## 📚 File Locations

- **Templates:** `shop/templates/shop/`
- **CSS:** `shop/static/shop/css/style.css`
- **JavaScript:** `shop/static/shop/js/script.js`
- **Models:** `shop/models.py`
- **Views:** `shop/views.py`
- **Admin Config:** `shop/admin.py`
- **URLs:** `shop/urls.py`

---

## 🎯 Next Steps

1. **Explore the site** - Click around, test features
2. **Add more products** - Build your catalog
3. **Upload images** - Make it look professional
4. **Test order flow** - Place orders and watch automation
5. **Customize design** - Edit CSS colors and styles
6. **Read README.md** - Detailed documentation
7. **Deploy to production** - See README for deployment guide

---

## 💡 Pro Tips

- **Cart works without login** - Great for user experience
- **Bulk actions save time** - Select multiple items in admin
- **Discount calculations are automatic** - Just set percentage
- **Orders auto-update** - Less manual work for admins
- **Scheduler must be running** - For automation to work
- **Images are optional** - Placeholder images work fine for testing

---

## ❓ Troubleshooting

### Can't access admin?
- URL: http://127.0.0.1:8000/admin
- Username: `admin`
- Password: `admin123`

### Products not showing?
- Run: `python manage.py create_sample_data`
- Or add manually via admin

### Orders not auto-updating?
- Make sure scheduler is running: `python manage.py run_scheduler`
- Check terminal for scheduler output

### Cart not working?
- Check browser console (F12) for errors
- Make sure JavaScript is loaded
- Clear browser cache

### Server not starting?
- Check if port 8000 is already in use
- Try: `python manage.py runserver 8080`

---

## 🎉 Enjoy DaeZone!

You're all set! Start exploring your e-commerce platform.

**Need help?** Check `README.md` for detailed documentation.

---

**DaeZone E-Commerce © 2026 | Built with Django**
