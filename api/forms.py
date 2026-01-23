from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import User as CustomUser, AuctionItem, Bid
from django.core.exceptions import ValidationError
from decimal import Decimal
from typing import Any, Dict


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Bootstrap-style styling"""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'id': 'email',
            'type': 'email',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'id': 'password',
        })

class CustomUserCreationForm(UserCreationForm):
    """Custom signup form with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'id': 'email',
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your first name',
            'id': 'firstName',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your last name',
            'id': 'lastName',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'id': 'password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'id': 'confirmPassword',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['username'].required = False

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
        return user


class AuctionForm(forms.Form):
    """Form for creating and validating auction items"""
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter auction title',
        })
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Enter detailed description',
            'rows': 4,
        })
    )
    starting_price = forms.DecimalField(
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99'),
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Starting price',
            'step': '0.01',
        })
    )
    image_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'Image URL (optional)',
        })
    )
    
    def clean_title(self) -> str:
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        return title.strip()
    
    def clean_description(self) -> str:
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 10:
            raise ValidationError("Description must be at least 10 characters long.")
        return description.strip()


class BidForm(forms.Form):
    """Form for validating bid amounts"""
    auction_id = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'type': 'hidden',
        })
    )
    bid_amount = forms.DecimalField(
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99'),
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your bid amount',
            'step': '0.01',
        })
    )
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.current_price = kwargs.pop('current_price', None)
        super().__init__(*args, **kwargs)
    
    def clean_bid_amount(self) -> Decimal:
        bid_amount = self.cleaned_data.get('bid_amount')
        
        if self.current_price is not None and bid_amount <= self.current_price:
            raise ValidationError(f"Bid must be higher than current price of ${self.current_price:.2f}")
        
        # Minimum bid increment of $0.01
        if self.current_price is not None and bid_amount < self.current_price + Decimal('0.01'):
            raise ValidationError("Bid must be at least $0.01 higher than current price")
            
        return bid_amount


class QuestionForm(forms.Form):
    """Form for asking questions about auctions"""
    auction_id = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'type': 'hidden',
        })
    )
    question_text = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Ask your question here...',
            'rows': 3,
        })
    )
    
    def clean_question_text(self) -> str:
        question = self.cleaned_data.get('question_text')
        if len(question.strip()) < 5:
            raise ValidationError("Question must be at least 5 characters long.")
        if len(question.strip()) > 1000:
            raise ValidationError("Question cannot exceed 1000 characters.")
        return question.strip()
