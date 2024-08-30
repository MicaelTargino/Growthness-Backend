from django.db import models
from authentication.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    daily_goal = models.FloatField()  # Could represent liters, steps, etc.
    measure = models.CharField(max_length=48, null=True) # define the measurement greatness of daily_goal (steps, liters, etc.)
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
