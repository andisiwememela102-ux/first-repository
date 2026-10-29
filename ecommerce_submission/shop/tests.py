from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Profile, Store, Product, Order, OrderItem, Review

class EcommerceTests(TestCase):
    """Exercise marketplace workflows and role permissions."""
    def setUp(self):
        """Create reusable buyer, vendor, store, and product fixtures."""
        self.vendor = User.objects.create_user(username='vendor', password='StrongPass123!')
        Profile.objects.create(user=self.vendor, role='vendor')
        self.store = Store.objects.create(owner=self.vendor, name='Test Store', description='A test store')
        self.product = Product.objects.create(store=self.store, name='Notebook', price=Decimal('25.00'), stock=10)
        self.buyer = User.objects.create_user(username='buyer', password='StrongPass123!', email='buyer@example.com')
        Profile.objects.create(user=self.buyer, role='buyer')
        self.client = Client()

    def test_home_shows_active_product(self):
        """Verify home shows active product."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notebook')

    def test_vendor_can_create_store(self):
        """Verify vendor can create store."""
        self.client.login(username='vendor', password='StrongPass123!')
        response = self.client.post(reverse('store_create'), {'name': 'Second Store', 'description': 'More goods'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Store.objects.filter(owner=self.vendor, name='Second Store').exists())

    def test_buyer_cannot_create_store(self):
        """Verify buyer cannot create store."""
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.get(reverse('store_create'))
        self.assertEqual(response.status_code, 403)

    def test_cart_add_and_checkout_decrements_stock_and_creates_invoice(self):
        """Verify cart add and checkout decrements stock and creates invoice."""
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
        """Verify cart rejects invalid quantity."""
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': 'not-a-number'})
        self.assertEqual(self.client.session['cart'][str(self.product.pk)], 1)

    def test_review_is_verified_after_purchase(self):
        """Verify review is verified after purchase."""
        order = Order.objects.create(buyer=self.buyer, invoice_number='INV-TEST-0001', total=Decimal('25.00'))
        OrderItem.objects.create(order=order, product=self.product, product_name=self.product.name, store_name=self.store.name, quantity=1, unit_price=self.product.price)
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('review_create', args=[self.product.pk]), {'rating': '5', 'comment': 'Good quality'})
        self.assertTrue(Review.objects.get(product=self.product, buyer=self.buyer).verified)

    def test_review_without_purchase_is_unverified(self):
        """Verify review without purchase is unverified."""
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('review_create', args=[self.product.pk]), {'rating': '4', 'comment': 'Looks good'})
        self.assertFalse(Review.objects.get(product=self.product, buyer=self.buyer).verified)

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        """Do not allow two accounts to share an email address."""
        response = self.client.post(reverse('register'), {
            'username': 'anotherbuyer', 'email': 'BUYER@example.com', 'role': 'buyer',
            'password1': 'StrongPass123!xyz', 'password2': 'StrongPass123!xyz',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email address already exists.')
        self.assertFalse(User.objects.filter(username='anotherbuyer').exists())

    def test_cart_has_continue_shopping_link(self):
        """Make the route back to product browsing obvious in the cart."""
        self.client.login(username='buyer', password='StrongPass123!')
        self.client.post(reverse('cart_add', args=[self.product.pk]), {'quantity': '1'})
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Continue Shopping')
        self.assertContains(response, reverse('home'))

    def test_buyer_can_edit_and_delete_own_review(self):
        """Allow a buyer to maintain their own review."""
        review = Review.objects.create(product=self.product, buyer=self.buyer, rating=3, comment='Okay')
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.post(reverse('review_edit', args=[review.pk]), {'rating': '5', 'comment': 'Excellent'})
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excellent')
        response = self.client.post(reverse('review_delete', args=[review.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_vendor_does_not_see_cart_navigation(self):
        """Keep buyer-only navigation hidden from vendor accounts."""
        self.client.login(username='vendor', password='StrongPass123!')
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, '>Cart</a>')

    def test_vendor_cannot_access_cart(self):
        """Restrict the cart page to authenticated buyers."""
        self.client.login(username='vendor', password='StrongPass123!')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 403)

    def test_empty_cart_offers_browsing_links(self):
        """Make it easy to return to the catalogue when the cart is empty."""
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Browse Stores')
        self.assertContains(response, 'Browse Products')

    def test_buyer_can_review_same_product_again_on_a_later_day(self):
        """Allow a buyer to add a new review after the previous review's day."""
        old_review = Review.objects.create(
            product=self.product, buyer=self.buyer, rating=2, comment='First impression'
        )
        Review.objects.filter(pk=old_review.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.post(
            reverse('review_create', args=[self.product.pk]),
            {'rating': '5', 'comment': 'I like it after using it'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.filter(product=self.product, buyer=self.buyer).count(), 2)

    def test_buyer_cannot_submit_two_reviews_for_same_product_on_same_day(self):
        """Prevent duplicate same-day reviews while preserving the first review."""
        Review.objects.create(
            product=self.product, buyer=self.buyer, rating=3, comment='Initial opinion'
        )
        self.client.login(username='buyer', password='StrongPass123!')
        response = self.client.post(
            reverse('review_create', args=[self.product.pk]),
            {'rating': '5', 'comment': 'Second opinion'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.filter(product=self.product, buyer=self.buyer).count(), 1)
        self.assertContains(response, 'already reviewed this product today')

