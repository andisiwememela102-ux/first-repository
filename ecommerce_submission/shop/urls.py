from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/new/', views.store_create, name='store_create'),
    path('stores/<int:store_id>/edit/', views.store_edit, name='store_edit'),
    path('stores/<int:store_id>/delete/', views.store_delete, name='store_delete'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('stores/<int:store_id>/products/new/', views.product_create, name='product_create'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:order_id>/', views.invoice, name='invoice'),
    path('products/<int:product_id>/review/', views.review_create, name='review_create'),
    path('reviews/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('password/forgot/', views.forgot_password, name='forgot_password'),
    path('password/reset/<str:token>/', views.reset_password, name='reset_password'),
]
