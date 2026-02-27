from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    """
    Custom user model that uses email as the primary authentication field
    instead of the default username.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email