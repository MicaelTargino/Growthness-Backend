from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from django.urls import reverse
from .models import UserGoals

class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.login_url = reverse('login')

        # Log in the user and obtain a token
        login_data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # Set token in the headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.complete_profile_url = reverse('complete-profile')
        self.goals_list_url = reverse('goals-list')

        # Create some test goals
        self.goal1 = UserGoals.objects.create(title='Run a marathon')
        self.goal2 = UserGoals.objects.create(title='Lose weight')

    def test_goals_list(self):
        # Test retrieving the list of goals
        response = self.client.get(self.goals_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Run a marathon')
        self.assertEqual(response.data[1]['title'], 'Lose weight')

    def test_complete_profile(self):
        # Test partially updating the user's profile (e.g., weight and goals)
        data = {
            'weight': 70.5,
            'height': 1.75,
            'goals_ids': [self.goal1.id, self.goal2.id]
        }
        response = self.client.patch(self.complete_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weight'], 70.5)
        self.assertEqual(response.data['height'], 1.75)
        self.assertEqual(len(response.data['goals']), 2)
        self.assertEqual(response.data['goals'][0], 'Run a marathon')
        self.assertEqual(response.data['goals'][1], 'Lose weight')

    def test_complete_profile_without_authentication(self):
        # Test completing the profile without authentication (should fail)
        self.client.logout()  # Remove authentication
        data = {
            'weight': 70.5,
            'height': 1.75,
            'goals_ids': [self.goal1.id, self.goal2.id]
        }
        response = self.client.patch(self.complete_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_complete_profile_partial_update(self):
        # Test partially updating only one field in the user's profile
        data = {
            'weight': 80.0
        }
        response = self.client.patch(self.complete_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['weight'], 80.0)

    def test_complete_profile_with_invalid_goal(self):
        # Test sending an invalid goal ID in the request
        data = {
            'weight': 70.5,
            'goals_ids': [9999]  # Non-existent goal ID
        }
        response = self.client.patch(self.complete_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IncompleteProfileTests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        
        # Create some goals for the test user
        self.goal1 = UserGoals.objects.create(title='Run a marathon')
        self.goal2 = UserGoals.objects.create(title='Lose weight')

        # Define the URL for incomplete profile check
        self.incomplete_profile_url = reverse('incomplete-profile', args=[self.user.id])

    def test_incomplete_profile_with_missing_fields(self):
        # Test case where the user profile is incomplete (missing weight, height, and goals)
        response = self.client.get(self.incomplete_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['profile_complete'])
        self.assertIn('weight', response.data['missing_fields'])
        self.assertIn('height', response.data['missing_fields'])
        self.assertIn('goals', response.data['missing_fields'])

    def test_complete_profile(self):
        # Test case where the profile is fully complete
        self.user.weight = 70.0
        self.user.height = 1.75
        self.user.goals.add(self.goal1)
        self.user.save()

        response = self.client.get(self.incomplete_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['profile_complete'])

    def test_profile_with_partial_completion(self):
        # Test case where the profile is partially completed (e.g., weight and height are filled, but goals are missing)
        self.user.weight = 70.0
        self.user.height = 1.75
        self.user.save()

        response = self.client.get(self.incomplete_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['profile_complete'])
        self.assertIn('goals', response.data['missing_fields'])
        self.assertNotIn('weight', response.data['missing_fields'])
        self.assertNotIn('height', response.data['missing_fields'])

    def test_incomplete_profile_with_invalid_user(self):
        # Test case where the user ID does not exist
        invalid_url = reverse('incomplete-profile', args=[9999])  # Non-existent user ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)