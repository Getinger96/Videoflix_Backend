from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    email = models.EmailField(unique=True)  # ✅ muss unique sein
    username = models.CharField(max_length=150, blank=True)  # optional, falls AbstractUser username braucht

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # username oder andere Felder, aber NICHT email



    def __str__(self):
        return self.email