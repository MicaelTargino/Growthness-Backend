from django.urls import path
from .views import FoodListCreateView, MealListCreateView, MealDetailView

urlpatterns = [
    path('foods/', FoodListCreateView.as_view(), name='food-list-create'),
    path('meals/', MealListCreateView.as_view(), name='meal-list-create'),
    path('meals/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
]
