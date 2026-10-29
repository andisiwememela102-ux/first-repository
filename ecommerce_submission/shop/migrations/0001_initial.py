# Initial schema for the MarketPlace application.
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    """Create the initial marketplace database schema."""

    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='PasswordResetToken', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('token_hash', models.CharField(max_length=64, unique=True)),
            ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ('expires_at', models.DateTimeField()), ('used', models.BooleanField(default=False)),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_tokens', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Profile', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('role', models.CharField(choices=[('buyer', 'Buyer'), ('vendor', 'Vendor')], default='buyer', max_length=10)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Store', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)), ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL)),
        ], options={'ordering': ['name']}),
        migrations.CreateModel(name='Product', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=120)), ('description', models.TextField(blank=True)),
            ('price', models.DecimalField(decimal_places=2, max_digits=10)), ('stock', models.PositiveIntegerField(default=0)),
            ('active', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
            ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.store')),
        ], options={'ordering': ['name']}),
        migrations.CreateModel(name='Order', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('created_at', models.DateTimeField(auto_now_add=True)), ('total', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)),
            ('invoice_number', models.CharField(max_length=32, unique=True)),
            ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='OrderItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('product_name', models.CharField(max_length=120)), ('store_name', models.CharField(max_length=120)),
            ('quantity', models.PositiveIntegerField()), ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='shop.product')),
        ]),
        migrations.CreateModel(name='Review', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
            ('comment', models.TextField(max_length=1000)), ('verified', models.BooleanField(default=False)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product')),
        ], options={'ordering': ['-created_at']}),
        migrations.AddConstraint(model_name='store', constraint=models.UniqueConstraint(fields=('owner', 'name'), name='unique_store_name_per_owner')),
        migrations.AddConstraint(model_name='product', constraint=models.UniqueConstraint(fields=('store', 'name'), name='unique_product_name_per_store')),
        migrations.AddConstraint(model_name='review', constraint=models.UniqueConstraint(fields=('product', 'buyer'), name='one_review_per_buyer_product')),
    ]
