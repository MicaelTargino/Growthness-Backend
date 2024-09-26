from django.contrib import admin
from .models import Meal, MealFood, Food
# Register your models here.
admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(MealFood)