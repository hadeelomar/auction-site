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
        ('cancelled', 'Cancelled'),
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
    
    winner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="won_auctions",
        help_text="Winner of the auction (set when auction closes)"
    )
    winning_bid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Final winning bid amount"
    )
    closed_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When the auction was closed"
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
            models.Index(fields=['winner']),
        ]

    def __str__(self):
        return self.title

    @property
    def end_datetime(self):
        """Alias for ends_at to match the management command"""
        return self.ends_at

    @property
    def seller(self):
        """Alias for owner to match the email templates"""
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
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()}"
