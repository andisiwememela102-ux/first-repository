from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Profile, Store, Product, Order, OrderItem, Review

class EcommerceTests(TestCase):
    def setUp(self):
        self.vendor = User.objects.create_user(username='vendor', password='StrongPass123!')
        Profile.objects.create(user=self.vendor, role='vendor')
        self.store = Store.objects.create(owner=self.vendor, name='Test Store', description='A test store')
        self.product = Product.objects.create(store=self.store, name='Notebook', price=Decimal('25.00'), stock=10)
        self.buyer = User.objects.create_user(username='buyer', password='StrongPass123!', email='buyer@example.com')
        Profile.objects.create(user=self.buyer, role='buyer')
        self.client = Client()

    def test_home_shows_active_product(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notebook')

    def test_vendor_can_create_store(self):
        self.client.login(username='vendor', password='StrongPass123!')
        response = self.client.post(reverse('store_create'), {'name': 'Second Store', 'description': 'More goods'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Store.objects.filter(owner=self.vendor, name='Second Store').exists())

    def test_buyer_cannot_create_store(self):
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.get(reverse('store_create'))
        self.assertEqual(response.status_code, 403)

    def test_cart_add_and_checkout_decrements_stock_and_creates_invoice(self):
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': '2'})
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        order = Order.objects.get(buyer=self.buyer)
        self.assertEqual(order.total, Decimal('50.00'))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(self.client.session.get('cart'), {})

    def test_cart_rejects_invalid_quantity(self):
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': 'not-a-number'})
        self.assertEqual(self.client.session['cart'][str(self.product.pk)], 1)

    def test_review_is_verified_after_purchase(self):
        order = Order.objects.create(buyer=self.buyer, invoice_number='INV-TEST-0001', total=Decimal('25.00'))
        OrderItem.objects.create(order=order, product=self.product, product_name=self.product.name, store_name=self.store.name, quantity=1, unit_price=self.product.price)
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('review_create', args=[self.product.pk]), {'rating': '5', 'comment': 'Good quality'})
        self.assertTrue(Review.objects.get(product=self.product, buyer=self.buyer).verified)

    def test_review_without_purchase_is_unverified(self):
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('review_create', args=[self.product.pk]), {'rating': '4', 'comment': 'Looks good'})
        self.assertFalse(Review.objects.get(product=self.product, buyer=self.buyer).verified)
