from django.db import models
from authentication.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField(help_text="Calories per serving")
    protein = models.FloatField(help_text="Protein content in grams per serving", blank=True, null=True)
    carbs = models.FloatField(help_text="Carbohydrates content in grams per serving", blank=True, null=True)
    fat = models.FloatField(help_text="Fat content in grams per serving", blank=True, null=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField()
    foods = models.ManyToManyField(Food, through='MealFood')

    def __str__(self):
        return f"{self.name} - {self.user.email} on {self.date}"


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.FloatField()

    def __str__(self):
        return f"{self.servings} servings of {self.food.name} in {self.meal.name}"
