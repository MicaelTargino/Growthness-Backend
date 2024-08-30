from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from django.urls import reverse
from .models import Habit, HabitLog
import datetime

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
        self.habit_log_url = reverse('habit-logs-list')

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

    def test_create_habit_log(self):
        # Test creating a habit log
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        data = {
            'habit': habit.id,
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'amount': 0.5
        }
        response = self.client.post(self.habit_log_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HabitLog.objects.count(), 1)
        self.assertEqual(HabitLog.objects.get().amount, 0.5)

    def test_list_habit_logs(self):
        # Test listing habit logs
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        HabitLog.objects.create(habit=habit, date=datetime.date.today().strftime('%Y-%m-%d'), amount=2.0)
        response = self.client.get(self.habit_log_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_habit_log(self):
        # Test retrieving a single habit log
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        habit_log = HabitLog.objects.create(habit=habit, date=datetime.date.today().strftime('%Y-%m-%d'), amount=2.0)
        response = self.client.get(reverse('habit-logs-detail', args=[habit_log.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 2.0)

    def test_update_habit_log(self):
        # Test updating a habit log
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        habit_log = HabitLog.objects.create(habit=habit, date=datetime.date.today().strftime('%Y-%m-%d'), amount=2.0)
        data = {
            'amount': 3.0
        }
        response = self.client.patch(reverse('habit-logs-detail', args=[habit_log.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit_log.refresh_from_db()
        self.assertEqual(habit_log.amount, 3.0)

    def test_delete_habit_log(self):
        # Test deleting a habit
        habit = Habit.objects.create(user=self.user, name='Drink Water', daily_goal=2.0)
        habit_log = HabitLog.objects.create(habit=habit, date=datetime.date.today().strftime('%Y-%m-%d'), amount=2.0)
        response = self.client.delete(reverse('habit-logs-detail', args=[habit_log.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HabitLog.objects.count(), 0)

    def test_habit_log_creation_without_authentication(self):
        # Test creating a habit log without authentication
        self.client.logout()
        data = {
            "habit": 1,
            "date": "2024-08-30",
            "amount": 0.5
        }
        response = self.client.post(self.habit_log_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)