from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from typing import Optional
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds the profile image and date of birth fields for our app.
    """

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True,
        help_text="User's profile picture",
    )

    date_of_birth = models.DateField(
        null=True, blank=True, help_text="User's date of birth"
    )

    preferred_currency = models.CharField(
        max_length=3,
        default='USD',
        choices=[
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
            ('JPY', 'Japanese Yen'),
            ('CNY', 'Chinese Yuan'),
            ('INR', 'Indian Rupee'),
            ('KRW', 'South Korean Won'),
            ('TRY', 'Turkish Lira'),
            ('RUB', 'Russian Ruble'),
            ('BRL', 'Brazilian Real'),
            ('MXN', 'Mexican Peso'),
            ('CAD', 'Canadian Dollar'),
            ('AUD', 'Australian Dollar'),
        ],
        help_text="User's preferred currency for display"
    )

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username

    @property
    def age(self) -> Optional[int]:
        """
        Computed property that calculates the user's age from their date of birth.
        """
        if self.date_of_birth:
            today = date.today()
            return (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
        return None

    def format_currency(self, amount: float) -> str:
        """
        Format amount according to user's preferred currency
        """
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'KRW': '₩',
            'TRY': '₺',
            'RUB': '₽',
            'BRL': 'R$',
            'MXN': '$',
            'CAD': 'C$',
            'AUD': 'A$',
        }
        
        symbol = currency_symbols.get(self.preferred_currency, '$')
        
        # Format with 2 decimal places for most currencies
        if self.preferred_currency in ['JPY', 'KRW']:
            # No decimal places for these currencies
            return f"{symbol}{int(amount):,}"
        else:
            return f"{symbol}{amount:,.2f}"


class AuctionItem(models.Model):
    """
    Auction Item model
    Includes the title, description, image, starting item
    """

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('sports', 'Sports'),
        ('art', 'Art'),
        ('vehicles', 'Vehicles'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='electronics')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Fields for auction closing
    winner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="won_auctions"
    )
    winning_bid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    closed_at = models.DateTimeField(
        null=True, 
        blank=True
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    class Meta:
        db_table = "auction_items"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['current_price']),
            models.Index(fields=['ends_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-ends_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    @property
    def end_datetime(self):
        """Alias for ends_at to match management command expectations"""
        return self.ends_at

    @property
    def seller(self):
        """Alias for owner to match management command expectations"""
        return self.owner


class Bid(models.Model):
    """
    Bid model for auction items.
    Tracks user bids with amount, timestamp, and winning status.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_winning = models.BooleanField(default=False)

    class Meta:
        db_table = "bids"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - ${self.bid_amount} on {self.item.title}"


class Question(models.Model):
    """
    Question model for auction item Q&A.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "questions"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username}: {self.question_text[:50]}"


class Reply(models.Model):
    """
    Reply model for Q&A questions.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    reply_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "replies"
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.user.username}: {self.reply_text[:50]}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('outbid', 'Outbid'),
        ('question_answered', 'Question Answered'),
        ('auction_ending', 'Auction Ending'),
        ('auction_won', 'Auction Won'),
        ('auction_lost', 'Auction Lost'),
        ('new_bid', 'New Bid'),
        ('new_question', 'New Question'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        db_table = "notifications"
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()}"
