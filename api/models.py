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
