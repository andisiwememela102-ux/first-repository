from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Store, Product, Review

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('vendor', 'Vendor')])
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'description')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock', 'active')
        widgets = {'price': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}), 'stock': forms.NumberInput(attrs={'min': 0})}
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
