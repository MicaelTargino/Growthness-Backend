from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.
class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)  # Make email unique

    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['password']  # Remove username from required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email