from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Exercise, Routine, RoutineExercise, ExerciseLog, Goal
from authentication.models import User

class ExerciseManagementTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.login_url = reverse('login')

        # Log in the user and obtain a token
        login_data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.exercise_url = reverse('exercise-list-create')
        self.routine_url = reverse('routine-list-create')
        self.exercise_log_url = reverse('exercise-log-list-create')
        self.goal_url = reverse('goal-list-create')

    def test_create_exercise(self):
        data = {
            'name': 'Running',
            'exercise_type': 'cardio',
            'duration': 30,
            'distance': 5.0,
            'average_velocity': 10.0,
            'pace': 6.0
        }
        response = self.client.post(self.exercise_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)

    def test_list_exercises(self):
        Exercise.objects.create(name='Running', exercise_type='cardio', duration=30)
        Exercise.objects.create(name='Weightlifting', exercise_type='gym', duration=45)
        response = self.client.get(self.exercise_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_exercise(self):
        exercise = Exercise.objects.create(name='Running', exercise_type='cardio', duration=30)
        response = self.client.get(reverse('exercise-detail', args=[exercise.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Running')

    def test_update_exercise(self):
        exercise = Exercise.objects.create(name='Running', exercise_type='cardio', duration=30)
        data = {'name': 'Cycling'}
        response = self.client.patch(reverse('exercise-detail', args=[exercise.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        exercise.refresh_from_db()
        self.assertEqual(exercise.name, 'Cycling')

    def test_delete_exercise(self):
        exercise = Exercise.objects.create(name='Running', exercise_type='cardio', duration=30)
        response = self.client.delete(reverse('exercise-detail', args=[exercise.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 0)

    def test_create_routine(self):
        data = {
            'user': self.user.id,  # Assuming you have a user field in the Routine model
            'week_start_date': '2024-09-01'
        }
        response = self.client.post(self.routine_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_exercise_log(self):
        exercise = Exercise.objects.create(name='Running', exercise_type='cardio', duration=30)
        routine = Routine.objects.create(user=self.user, week_start_date='2024-09-01')
        routine_exercise = RoutineExercise.objects.create(routine=routine, exercise=exercise)

        data = {
            'routine_exercise': routine_exercise.id,
            'user': self.user.id,  # Add the user field
            'date_logged': '2024-09-01',  # Ensure this field exists in the ExerciseLog model
            'weight': 0,
            'reps': 0,
            'distance_logged': 5.0,
            'average_velocity_logged': 10.0,
            'pace_logged': 6.0
        }
        response = self.client.post(self.exercise_log_url, data, format='json')
        
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Print the response data to help debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_goal(self):
        data = {
            'user': self.user.id,  # Assuming you have a user field in the Goal model
            'description': 'Run a marathon',
            'target_date': '2024-12-31'
        }
        response = self.client.post(self.goal_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_goal_list(self):
        Goal.objects.create(user=self.user, description='Run a marathon', target_date='2024-12-31')
        response = self.client.get(self.goal_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_goal_update(self):
        goal = Goal.objects.create(user=self.user, description='Run a marathon', target_date='2024-12-31')
        data = {'description': 'Train for a marathon'}
        response = self.client.patch(reverse('goal-detail', args=[goal.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.description, 'Train for a marathon')

    def test_goal_delete(self):
        goal = Goal.objects.create(user=self.user, description='Run a marathon', target_date='2024-12-31')
        response = self.client.delete(reverse('goal-detail', args=[goal.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Goal.objects.count(), 0)

    def test_create_exercise_without_authentication(self):
        self.client.logout()
        data = {
            'name': 'Running',
            'exercise_type': 'cardio',
            'duration': 30
        }
        response = self.client.post(self.exercise_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
