from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from authentication.models import User
from .models import Food, Meal, MealFood

class DietTrackingTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.login_url = reverse('login')

        # Log in the user and obtain a token
        login_data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.food_url = reverse('food-list-create')
        self.meal_url = reverse('meal-list-create')

    def test_create_food(self):
        data = {
            'name': 'Banana',
            'calories': 89,
            'protein': 1.1,
            'carbs': 22.8,
            'fat': 0.3
        }
        response = self.client.post(self.food_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Food.objects.count(), 1)

    def test_create_meal_with_foods(self):
        food = Food.objects.create(name='Banana', calories=89)
        data = {
            'name': 'Breakfast',
            'date': '2024-09-26',
            'foods': [{'food': food.id, 'servings': 2}]
        }
        response = self.client.post(self.meal_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertEqual(MealFood.objects.count(), 1)

    def test_list_meals(self):
        meal = Meal.objects.create(name='Breakfast', user=self.user, date='2024-09-26')
        MealFood.objects.create(meal=meal, food=Food.objects.create(name='Apple', calories=52), servings=1)

        response = self.client.get(self.meal_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
