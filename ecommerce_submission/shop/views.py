import hashlib
import secrets
from functools import wraps
from datetime import timedelta
from decimal import Decimal
from uuid import uuid4
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import RegistrationForm, StoreForm, ProductForm, ReviewForm
from .models import Profile, Store, Product, Order, OrderItem, Review, PasswordResetToken


def role_of(user):
    """Return the role assigned to a user, defaulting to buyer."""
    return getattr(getattr(user, 'profile', None), 'role', 'buyer')

def vendor_required(view_func):
    """Restrict a view to authenticated vendor accounts."""
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        """Check the current account role before calling the wrapped view."""
        if role_of(request.user) != 'vendor':
            return HttpResponseForbidden('Only vendor accounts can manage stores and products.')
        return view_func(request, *args, **kwargs)
    return wrapped

def buyer_required(view_func):
    """Restrict a view to authenticated buyer accounts."""
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        """Check the current account role before calling the wrapped view."""
        if role_of(request.user) != 'buyer':
            return HttpResponseForbidden('Only buyer accounts can use this feature.')
        return view_func(request, *args, **kwargs)
    return wrapped

def home(request):
    """Display active, in-stock products on the marketplace homepage."""
    products = Product.objects.filter(active=True, stock__gt=0).select_related('store', 'store__owner')
    return render(request, 'shop/home.html', {'products': products})

def register(request):
    """Create a buyer or vendor account after validating registration details."""
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, role=form.cleaned_data['role'])
        login(request, user)
        messages.success(request, 'Your account has been created.')
        return redirect('home')
    return render(request, 'shop/form.html', {'form': form, 'title': 'Create an account'})

def login_view(request):
    """Authenticate a user and start their session."""
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username', '').strip(), password=request.POST.get('password', ''))
        if user is not None:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('home')
        error = 'The username or password was not recognised.'
    return render(request, 'shop/login.html', {'error': error})

def logout_view(request):
    """End the current session when a POST request is submitted."""
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def store_list(request):
    """Display all marketplace stores."""
    return render(request, 'shop/store_list.html', {'stores': Store.objects.select_related('owner').all()})

def store_detail(request, store_id):
    """Display a store and its active products."""
    store = get_object_or_404(Store, pk=store_id)
    products = store.products.filter(active=True)
    return render(request, 'shop/store_detail.html', {'store': store, 'products': products})

@vendor_required
def store_create(request):
    """Create a store owned by the signed-in vendor."""
    form = StoreForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        store = form.save(commit=False); store.owner = request.user; store.save()
        messages.success(request, 'Store created.')
        return redirect('store_detail', store_id=store.pk)
    return render(request, 'shop/form.html', {'form': form, 'title': 'Create store'})

@vendor_required
def store_edit(request, store_id):
    """Update a store owned by the signed-in vendor."""
    store = get_object_or_404(Store, pk=store_id, owner=request.user)
    form = StoreForm(request.POST or None, instance=store)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Store updated.'); return redirect('store_detail', store_id=store.pk)
    return render(request, 'shop/form.html', {'form': form, 'title': 'Edit store'})

@vendor_required
def store_delete(request, store_id):
    """Delete a vendor-owned store after confirmation."""
    store = get_object_or_404(Store, pk=store_id, owner=request.user)
    if request.method == 'POST':
        store.delete(); messages.success(request, 'Store deleted.'); return redirect('store_list')
    return render(request, 'shop/confirm_delete.html', {'object': store, 'cancel_url': 'store_detail', 'cancel_id': store.pk})

@vendor_required
def product_create(request, store_id):
    """Add a product to a store owned by the signed-in vendor."""
    store = get_object_or_404(Store, pk=store_id, owner=request.user)
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False); product.store = store; product.save()
        messages.success(request, 'Product added.'); return redirect('product_detail', product_id=product.pk)
    return render(request, 'shop/form.html', {'form': form, 'title': f'Add product to {store.name}'})

def product_detail(request, product_id):
    """Display product details and its reviews."""
    product = get_object_or_404(Product.objects.select_related('store', 'store__owner'), pk=product_id, active=True)
    return render(request, 'shop/product_detail.html', {'product': product, 'reviews': product.reviews.select_related('buyer')})

@vendor_required
def product_edit(request, product_id):
    """Update a product belonging to the signed-in vendor."""
    product = get_object_or_404(Product, pk=product_id, store__owner=request.user)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Product updated.'); return redirect('product_detail', product_id=product.pk)
    return render(request, 'shop/form.html', {'form': form, 'title': 'Edit product'})

@vendor_required
def product_delete(request, product_id):
    """Delete a product belonging to the signed-in vendor."""
    product = get_object_or_404(Product, pk=product_id, store__owner=request.user)
    if request.method == 'POST':
        product.delete(); messages.success(request, 'Product deleted.'); return redirect('store_detail', store_id=product.store_id)
    return render(request, 'shop/confirm_delete.html', {'object': product, 'cancel_url': 'product_detail', 'cancel_id': product.pk})

def _cart(request):
    """Return a cleaned cart mapping product IDs to positive quantities.

    Invalid or corrupted session data is ignored so a stale cart cannot crash
    the cart page or checkout workflow.
    """
    raw = request.session.get('cart', {})
    if not isinstance(raw, dict):
        return {}
    cleaned = {}
    for key, value in raw.items():
        key_text, value_text = str(key), str(value)
        if key_text.isdigit() and value_text.isdigit() and int(value_text) > 0:
            cleaned[key_text] = min(int(value_text), 999)
    return cleaned

@buyer_required
def cart_view(request):
    """Display cart items, totals, and shopping/checkout actions."""
    cart = _cart(request)
    rows = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=int(product_id), active=True).first()
        if product:
            line_total = product.price * quantity
            rows.append({'product': product, 'quantity': quantity, 'line_total': line_total})
            total += line_total
    return render(request, 'shop/cart.html', {'rows': rows, 'total': total})

@buyer_required
def cart_add(request, product_id):
    """Add an in-stock product to the authenticated buyer cart."""
    if request.method != 'POST': return redirect('product_detail', product_id=product_id)
    product = get_object_or_404(Product, pk=product_id, active=True)
    try: quantity = int(request.POST.get('quantity', '1'))
    except (ValueError, TypeError): quantity = 1
    quantity = max(1, min(quantity, 999))
    cart = _cart(request); new_quantity = cart.get(str(product.pk), 0) + quantity
    if product.stock < 1:
        messages.error(request, 'This product is out of stock.')
    elif new_quantity > product.stock:
        messages.error(request, f'Only {product.stock} item(s) are currently in stock.')
    else:
        cart[str(product.pk)] = new_quantity; request.session['cart'] = cart; request.session.modified = True
        messages.success(request, 'Product added to your cart.')
    return redirect('cart')

@buyer_required
def cart_update(request, product_id):
    """Update the quantity of a product in the buyer cart."""
    if request.method == 'POST':
        cart = _cart(request)
        try:
            quantity = int(request.POST.get('quantity', '1'))
        except (ValueError, TypeError):
            quantity = 1
        quantity = min(quantity, 999)
        product = Product.objects.filter(pk=product_id, active=True).first()
        if quantity < 1: cart.pop(str(product_id), None)
        elif product and quantity <= product.stock: cart[str(product_id)] = quantity
        else: messages.error(request, 'Requested quantity is not available.')
        request.session['cart'] = cart; request.session.modified = True
    return redirect('cart')

@buyer_required
def cart_remove(request, product_id):
    """Remove a product from the buyer cart."""
    if request.method == 'POST':
        cart = _cart(request); cart.pop(str(product_id), None)
        request.session['cart'] = cart; request.session.modified = True
    return redirect('cart')

@buyer_required
def checkout(request):
    """Validate the cart and create an order while reducing stock."""
    if request.method != 'POST': return redirect('cart')
    cart = _cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty.'); return redirect('cart')
    try:
        with transaction.atomic():
            products = {}
            for pid, qty in cart.items():
                product = Product.objects.select_for_update().select_related('store').filter(pk=int(pid), active=True).first()
                if not product or qty > product.stock:
                    raise ValueError('One or more products are no longer available in the requested quantity. Please review your cart.')
                products[pid] = (product, qty)
            order = Order.objects.create(buyer=request.user, invoice_number=f'INV-{timezone.now():%Y%m%d}-{uuid4().hex[:8].upper()}')
            total = Decimal('0.00')
            for product, qty in products.values():
                OrderItem.objects.create(order=order, product=product, product_name=product.name,
                    store_name=product.store.name, quantity=qty, unit_price=product.price)
                product.stock -= qty; product.save(update_fields=['stock'])
                total += product.price * qty
            order.total = total; order.save(update_fields=['total'])
    except ValueError as exc:
        messages.error(request, str(exc)); return redirect('cart')
    request.session['cart'] = {}; request.session.modified = True
    invoice_lines = [f'{item.product_name} ({item.store_name}) x {item.quantity}: R{item.line_total:.2f}' for item in order.items.all()]
    body = f"Thank you for your order. Invoice: {order.invoice_number}\n\n" + '\n'.join(invoice_lines) + f'\n\nTotal: R{order.total:.2f}'
    if request.user.email:
        try: send_mail(f'Your eCommerce invoice {order.invoice_number}', body, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=True)
        except Exception: pass
    messages.success(request, 'Checkout complete. Your invoice has been created and sent when email is configured.')
    return redirect('invoice', order_id=order.pk)

@login_required
def invoice(request, order_id):
    """Display an invoice belonging to the signed-in buyer."""
    order = get_object_or_404(Order.objects.prefetch_related('items'), pk=order_id, buyer=request.user)
    return render(request, 'shop/invoice.html', {'order': order})

@buyer_required
def review_create(request, product_id):
    """Create a review, preventing duplicate submissions on the same day."""
    product = get_object_or_404(Product, pk=product_id, active=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            today = timezone.localdate()
            reviewed_today = Review.objects.filter(
                product=product, buyer=request.user, created_at__date=today
            ).exists()
            if reviewed_today:
                messages.error(request, 'You have already reviewed this product today. You can edit your existing review instead.')
            else:
                verified = OrderItem.objects.filter(order__buyer=request.user, product=product).exists()
                review = form.save(commit=False)
                review.product = product
                review.buyer = request.user
                review.verified = verified
                review.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect('product_detail', product_id=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'shop/form.html', {'form': form, 'title': f'Review {product.name}'})


@buyer_required
def review_edit(request, review_id):
    """Update a review only when it belongs to the signed-in buyer."""
    review = get_object_or_404(Review, pk=review_id, buyer=request.user)
    form = ReviewForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your review has been updated.')
        return redirect('product_detail', product_id=review.product_id)
    return render(request, 'shop/form.html', {'form': form, 'title': f'Edit review for {review.product.name}'})


@buyer_required
def review_delete(request, review_id):
    """Delete a review only when it belongs to the signed-in buyer."""
    review = get_object_or_404(Review, pk=review_id, buyer=request.user)
    product_id = review.product_id
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('product_detail', product_id=product_id)
    return render(request, 'shop/confirm_delete.html', {
        'object': review, 'cancel_url': 'product_detail', 'cancel_id': product_id,
    })

def forgot_password(request):
    """Send a time-limited password-reset link without revealing account existence."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        # Use the same response whether the account exists or not to avoid leaking accounts.
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            raw_token = secrets.token_urlsafe(32)
            PasswordResetToken.objects.create(user=user, token_hash=hashlib.sha256(raw_token.encode()).hexdigest(), expires_at=timezone.now() + timedelta(minutes=15))
            reset_url = request.build_absolute_uri(f'/password/reset/{raw_token}/')
            send_mail('Reset your password', f'Use this link within 15 minutes to reset your password:\n{reset_url}', settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        messages.success(request, 'If an account uses that email address, a password reset link has been sent.')
        return redirect('login')
    return render(request, 'shop/forgot_password.html')

def reset_password(request, token):
    """Validate a reset token and update the associated account password."""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    reset = PasswordResetToken.objects.select_related('user').filter(token_hash=token_hash).first()
    if not reset or not reset.is_valid():
        return render(request, 'shop/reset_password.html', {'invalid': True})
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm = request.POST.get('password_confirm', '')
        if password != confirm:
            return render(request, 'shop/reset_password.html', {'error': 'The passwords do not match.'})
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        try: validate_password(password, reset.user)
        except ValidationError as exc:
            return render(request, 'shop/reset_password.html', {'error': ' '.join(exc.messages)})
        reset.user.set_password(password); reset.user.save(update_fields=['password'])
        reset.used = True; reset.save(update_fields=['used'])
        messages.success(request, 'Password changed. Please log in with your new password.')
        return redirect('login')
    return render(request, 'shop/reset_password.html')
