# Luminary — Django E-Commerce App

A complete, production-ready Django e-commerce application with a clean, modern UI.

## Features

- **Product catalog** — categories, search, sorting, featured products
- **Product detail** — images, stock tracking, discount badges, star reviews
- **Shopping cart** — session-based for guests, user-linked after login
- **Checkout** — shipping form, order creation, stock decrement
- **Order management** — order history, status tracking, detailed receipts
- **User auth** — register, login, profile page
- **Admin panel** — full CRUD for products, orders, categories, reviews
- **Sample data** — seed command to populate 10 products across 4 categories

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed sample products
python manage.py seed_data

# 5. Create a superuser (for the admin panel)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to see the store.
Visit **http://127.0.0.1:8000/admin** to manage products and orders.

## Project Structure

```
ecommerce/
├── ecommerce/          # Django project settings & URL root
│   ├── settings.py
│   └── urls.py
├── store/              # Main app
│   ├── models.py       # Category, Product, Cart, Order, Review
│   ├── views.py        # All view logic
│   ├── forms.py        # Auth, checkout, review forms
│   ├── urls.py         # URL patterns
│   ├── admin.py        # Admin config
│   ├── context_processors.py  # Cart count in nav
│   ├── templates/store/       # All HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_list.html
│   │   ├── order_detail.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── management/commands/
│       └── seed_data.py
├── media/              # Uploaded product images
├── static/             # CSS/JS/images
├── requirements.txt
└── manage.py
```

## Models

| Model      | Key fields                                                   |
|------------|--------------------------------------------------------------|
| Category   | name, slug, description                                      |
| Product    | name, slug, price, original_price, stock, is_featured, image |
| Cart       | user (OneToOne), session_key                                 |
| CartItem   | cart, product, quantity                                      |
| Order      | user, status, shipping fields, total_price                   |
| OrderItem  | order, product, product_name (snapshot), price, quantity     |
| Review     | product, user, rating (1-5), comment                         |

## Extending the App

- **Payments**: Integrate Stripe via `stripe` Python SDK at the checkout view
- **Email notifications**: Add `post_save` signal on Order to send confirmation
- **Pagination**: Wrap product QuerySets with Django's `Paginator`
- **Wishlists**: Add a `ManyToManyField(Product)` on a UserProfile model
- **Image uploads**: Products support image upload via the admin — set `MEDIA_ROOT` for production

## Deployment Notes

For production, set in `settings.py`:
```python
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['yourdomain.com']
```

Use `whitenoise` for static files and a cloud storage backend (e.g. S3) for media.
