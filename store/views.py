from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review
from .forms import (
    RegisterForm, LoginForm, CheckoutForm, ReviewForm, ProductSearchForm
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ─── Store Pages ─────────────────────────────────────────────────────────────

def home(request):
    featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    new_arrivals = Product.objects.filter(is_active=True)[:6]
    return render(request, 'store/home.html', {
        'featured': featured,
        'categories': categories,
        'new_arrivals': new_arrivals,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    form = ProductSearchForm(request.GET or None)

    category_slug = request.GET.get('category')
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'newest')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    sort_map = {
        'newest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    active_category = None
    if category_slug:
        active_category = categories.filter(slug=category_slug).first()

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'query': query,
        'sort': sort,
        'form': form,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.select_related('user')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    review_form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated and not user_review:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            r = review_form.save(commit=False)
            r.product = product
            r.user = request.user
            r.save()
            messages.success(request, 'Review submitted!')
            return redirect(product.get_absolute_url())

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related': related,
        'review_form': review_form,
        'user_review': user_review,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'store/category.html', {
        'category': category,
        'products': products,
    })


# ─── Cart ────────────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)
    qty = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()

    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.POST.get('next', 'store:cart'))


def cart_update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('store:cart')


def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('store:cart')


# ─── Checkout & Orders ───────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    form = CheckoutForm(request.POST or None, initial={
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
    })

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total,
            postal_code='',
            country='Uganda',
            **form.cleaned_data,
        )
        for ci in cart.items.select_related('product'):
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                product_name=ci.product.name,
                price=ci.product.price,
                quantity=ci.quantity,
            )
            # Decrement stock
            ci.product.stock = max(0, ci.product.stock - ci.quantity)
            ci.product.save()
        cart.items.all().delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('store:order_detail', pk=order.pk)

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


# ─── Auth ────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}!')
        return redirect('store:home')
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'store:home'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('store:home')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)[:5]
    return render(request, 'store/profile.html', {
        'user': request.user,
        'orders': orders,
    })
