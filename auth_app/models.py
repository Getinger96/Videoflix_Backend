from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    """
    Custom user model that uses email as the primary authentication field
    instead of the default username.
    """

    email = models.EmailField(unique=True)
    """The user's email address. Must be unique and is used as the login identifier."""

    username = models.CharField(max_length=150, blank=True)
    """Optional username field. Kept for compatibility with AbstractUser but not required."""

    USERNAME_FIELD = 'email'
    """Defines email as the unique identifier for authentication instead of username."""

    REQUIRED_FIELDS = []
    """No additional fields are required when creating a user via createsuperuser."""

    def __str__(self):
        """
        Return the string representation of the user.

        :return: The user's email address
        """
        return self.email