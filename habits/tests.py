from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from django.urls import reverse
from .models import Habit

class HabitTests(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')

        # Create a user and obtain a token for authentication
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        
        # Log in the user and obtain a token
        login_data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # Step 2: Set token in the headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.habit_url = reverse('habits-list')  # Use the name of your route

    def test_create_habit(self):
        # Test creating a habit
        data = {
            'name': 'Drink Water',
            'daily_goal': 2.0
        }
        response = self.client.post(self.habit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().name, 'Drink Water')

    def test_list_habits(self):
        # Test listing habits
        Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        Habit.objects.create(user=self.user, name='Exercise', daily_goal=1.0)
        response = self.client.get(self.habit_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_habit(self):
        # Test retrieving a single habit
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        response = self.client.get(reverse('habits-detail', args=[habit.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Drink Water')

    def test_update_habit(self):
        # Test updating a habit
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        data = {
            'name': 'Drink More Water',
            'daily_goal': 3.0
        }
        response = self.client.patch(reverse('habits-detail', args=[habit.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.name, 'Drink More Water')
        self.assertEqual(habit.daily_goal, 3.0)

    def test_delete_habit(self):
        # Test deleting a habit
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        response = self.client.delete(reverse('habits-detail', args=[habit.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_creation_without_authentication(self):
        # Test creating a habit without authentication
        self.client.logout()
        data = {
            'name': 'Drink Water',
            'daily_goal': 2.0
        }
        response = self.client.post(self.habit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
