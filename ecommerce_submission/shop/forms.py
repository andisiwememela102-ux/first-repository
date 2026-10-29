from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Store, Product, Review

class RegistrationForm(UserCreationForm):
    """Collect account details and enforce unique email addresses."""

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('vendor', 'Vendor')])
    class Meta:
        """Configure the user fields displayed during registration."""

        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        """Reject email addresses already used by another account."""
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email address already exists.')
        return email

class StoreForm(forms.ModelForm):
    """Validate store details supplied by a vendor."""

    class Meta:
        """Select the editable store fields."""
        model = Store
        fields = ('name', 'description')

class ProductForm(forms.ModelForm):
    """Validate product information and pricing."""

    class Meta:
        """Select product fields and input widgets."""
        model = Product
        fields = ('name', 'description', 'price', 'stock', 'active')
        widgets = {'price': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}), 'stock': forms.NumberInput(attrs={'min': 0})}
    def clean_price(self):
        """Require product prices to be positive."""
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

class ReviewForm(forms.ModelForm):
    """Validate a product rating and review comment."""

    class Meta:
        """Select fields that buyers may include in a review."""
        model = Review
        fields = ('rating', 'comment')
