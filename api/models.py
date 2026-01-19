from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from typing import Optional


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

    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    class Meta:
        db_table = "auction_items"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


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
