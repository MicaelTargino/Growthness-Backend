from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import password_reset_token

class testuserAuthentication(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword123')

        # URLs for your endpoints
        self.password_reset_request_url = reverse('password-reset-request')
        self.password_reset_confirm_url = reverse('password-reset-confirm')
        self.change_password_url = reverse('change-password')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_password_reset_request(self):
        data = {'email': 'testuser@example.com', 'test': True}
        response = self.client.post(self.password_reset_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_request_invalid_email(self):
        data = {'email': 'invalid-email@example.com'}
        response = self.client.post(self.password_reset_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "There is no user registered with this email address.")

    def test_password_reset_request_no_data(self):
        response = self.client.post(self.password_reset_request_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_password_reset_confirm(self):
        # Generate a valid token and UID
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = password_reset_token.make_token(self.user)
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify password was updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_reset_confirm_no_data(self):
        response = self.client.post(self.password_reset_confirm_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('uid', response.data)
        self.assertIn('token', response.data)
        self.assertIn('new_password', response.data)
        self.assertIn('confirm_password', response.data)

    def test_password_reset_confirm_mismatched_passwords(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = password_reset_token.make_token(self.user)
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword456'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "Passwords do not match.")

    def test_password_reset_confirm_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {
            'uid': uid,
            'token': 'invalid-token',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        login_data = {'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword456',
            'confirm_password': 'newpassword456'
        }

        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify password was updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword456'))

    def test_change_password_no_data(self):
        login_data = {'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # Step 2: Set token in the headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.change_password_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_incorrect_old_password(self):
        login_data = {'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword456',
            'confirm_password': 'newpassword456'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['old_password'][0], "Old password is not correct.")

    def test_change_password_mismatched_passwords(self):
        login_data = {'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # Step 2: Set token in the headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword456',
            'confirm_password': 'differentpassword789'
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], "The new passwords do not match.")

    def test_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if token is in the response
        self.assertIn('access', response.data)

    def test_login_no_data(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        # Step 1: Log in the user and obtain a token
        login_data = {'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        refresh_token = response.data['refresh']
        data = {'refresh_token': refresh_token}

        # Step 2: Set token in the headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Step 3: Ensure the user can access a protected endpoint
        protected_response = self.client.get(reverse('protected-endpoint'))
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

        # Step 4: Log out the user
        logout_response = self.client.post(self.logout_url, data)
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

        self.client.credentials()
        # Step 5: Attempt to access a protected endpoint with the same token
        protected_response_after_logout = self.client.get(reverse('protected-endpoint'))
        self.assertEqual(protected_response_after_logout.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_not_logged_in(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

