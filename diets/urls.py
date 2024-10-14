from django.urls import path
from .views import FoodListCreateView, MealListCreateView, MealDetailView, MealFoodsListView

urlpatterns = [
    path('foods/', FoodListCreateView.as_view(), name='food-list-create'),
    path('meals/', MealListCreateView.as_view(), name='meal-list-create'),
    path('meals/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('meals/<int:meal_id>/foods/', MealFoodsListView.as_view(), name='meal-foods-list'),
]
