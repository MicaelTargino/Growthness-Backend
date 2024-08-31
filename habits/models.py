from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError

class Frequency(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    name = models.CharField(
        max_length=8,
        choices=FREQUENCY_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goal = models.FloatField()  # Could represent liters, steps, etc.
    measure = models.CharField(max_length=48, null=True) # define the measurement greatness of goal (steps, liters, etc.)
    frequencies = models.ManyToManyField(Frequency)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s habit: {self.name}"

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()  # Amount of water, steps, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.name} on {self.date}"
