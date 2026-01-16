from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
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
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username

    def age(self) -> Optional[int]:
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
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        db_table = "auction_items"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
