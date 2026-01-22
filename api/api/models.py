from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime
from typing import Optional


class User(AbstractUser):
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

    def __str__(self):
        return self.username

    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            today = date.today()
            return (
                today.year
                - self.date_of_birth.year
                - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            )
        return None


class AuctionItem(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(db_index=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    # --- Task 11 Enhancements ---
    winner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="won_auctions"
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    watchers = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlist"
    )

    class Meta:
        db_table = "auction_items"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["description"]),
            models.Index(fields=["ends_at"]),
            models.Index(fields=["current_price"]),
        ]

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.closed_at:
            return "closed"
        if self.ends_at and self.ends_at < datetime.now().astimezone():
            return "finished"
        return "active"


class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bids"
        ordering = ["-placed_at"]

    def __str__(self):
        return f"{self.bidder.username} - {self.amount}"


class Question(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="questions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email}: {self.text[:30]}"


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.email}: {self.text[:30]}"
