from django.contrib import admin
from .models import Profile, Store, Product, Order, OrderItem, Review, PasswordResetToken

admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(PasswordResetToken)
