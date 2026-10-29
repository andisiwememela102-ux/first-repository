from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    """Store the marketplace role associated with a user account."""
    BUYER = 'buyer'
    VENDOR = 'vendor'
    ROLE_CHOICES = [(BUYER, 'Buyer'), (VENDOR, 'Vendor')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)

    def __str__(self):
        """Return a readable account and role label."""
        return f'{self.user.username} ({self.role})'

class Store(models.Model):
    """Represent a vendor-owned store in the marketplace."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering and database constraints."""
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['owner', 'name'], name='unique_store_name_per_owner')]

    def __str__(self):
        """Return the store name."""
        return self.name

class Product(models.Model):
    """Represent an item listed by a store."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering and database constraints."""
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=['store', 'name'], name='unique_product_name_per_store')]

    def __str__(self):
        """Return the product and its store name."""
        return f'{self.name} ({self.store.name})'

class Order(models.Model):
    """Record a completed buyer checkout."""
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    invoice_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        """Return the order invoice number."""
        return self.invoice_number

class OrderItem(models.Model):
    """Store a product snapshot and quantity for an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    product_name = models.CharField(max_length=120)
    store_name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        """Calculate the total cost of this order line."""
        return self.unit_price * self.quantity

class Review(models.Model):
    """Represent one buyer review; buyers may update it over time."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(max_length=1000)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering and database constraints."""
        ordering = ['-created_at']

    def __str__(self):
        """Return a concise review description."""
        return f'{self.product.name}: {self.rating}/5 by {self.buyer.username}'

class PasswordResetToken(models.Model):
    """Store a hashed, expiring password-reset token."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reset_tokens')
    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        """Return whether the token is unused and has not expired."""
        return not self.used and timezone.now() < self.expires_at
