from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from typing import Optional
from decimal import Decimal


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser. Includes profile image, email and date of birth."""

    profile_image = ImageField(
        upload_to="profile_images/",
        null=True,
        blank=False,
        default="profile_images/default.jpg",
    )
    email = models.EmailField(unique=True, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.username} {self.email}"


class Item(models.Model):
    """Auction item model - represents items users can auction"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    picture = models.ImageField(upload_to="item_images/", null=True, blank=True)
    end_datetime = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} - ${self.starting_price}"

    def is_auction_ended(self) -> bool:
        """Checks is auction has ended"""
        return timezone.now() > self.end_datetime

    def get_current_highest_bid(self) -> Optional[Decimal]:
        """Gets the current highest bid amount for this item"""
        highest_bid = self.bids.order_by("-amount").first()
        return highest_bid.amount if highest_bid else self.starting_price

    def get_highest_bidder(self) -> Optional[User]:
        """Gets the user with the highest bid"""
        highest_bid = self.bids.order_by("-amount").first()
        return highest_bid.bidder if highest_bid else None

    def get_bid_count(self) -> int:
        """Gets the total number of bids for this item"""
        return self.bids.count()


class Bid(models.Model):
    """Bid model for auction items. Tracks all bids placed by users on items"""

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.bidder.username} bid ${self.amount} on {self.item.title}"

    def clean(self) -> None:
        """Validate bid before saving"""
        if self.item.is_auction_ended():
            raise ValidationError("Can't bid on an auction that has ended.")

        current_highest = self.item.get_current_highest_bid()
        if current_highest and self.amount <= current_highest:
            raise ValidationError(
                f"Bid must be higher than the current highest bid of ${current_highest}"
            )

        if self.amount < self.item.starting_price:
            raise ValidationError(f"Bid must be at least ${self.item.starting_price}")

    def save(self, *args, **kwargs) -> None:
        """Override save to run validation"""
        self.full_clean()
        super().save(*args, **kwargs)


class Question(models.Model):
    """
    Question model for items. Users can ask questions about items
    they''re interested in.
    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="questions")
    asker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="questions_asked"
    )
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Q by {self.asker.username} on {self.item.title}"

    def has_reply(self) -> bool:
        """Check if question has been answered"""
        return hasattr(self, "reply") and self.reply is not None


class Reply(models.Model):
    """
    Reply/answer model for questions. Item owners can reply to
    questions about their items.
    """

    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name="reply"
    )
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Reply to Question #{self.question.id}"

    def clean(self) -> None:
        """Validate that only item owner can reply"""
        if not self.answer_text.strip():
            raise ValidationError("Reply can't be empty")

    def save(self, *args, **kwargs) -> None:
        """Override save to run validation"""
        self.full_clean()
        super().save(*args, **kwargs)


class AuctionWinnerNotification(models.Model):
    """
    Track email notification sent to auction winners. Used by cron jobs to
    ensure emails are sent once.
    """

    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, related_name="winner_notification"
    )
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won_auctions"
    )
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.winner.username} won {self.item.title} - Email sent: {self.email_sent}"
