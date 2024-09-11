from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from complete_profile.models import UserGoals
# Create your models here.

class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)  # Make email unique
    
    weight = models.FloatField(null=True, blank=True)
    weight_measure = models.CharField(max_length=20, default="kg")

    height = models.FloatField(null=True, blank=True)
    height_measure = models.CharField(max_length=20, default="m")

    goals = models.ManyToManyField(UserGoals, blank=True, null=True, related_name="user_goals")

    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['password']  # Remove username from required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email