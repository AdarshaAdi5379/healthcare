from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.valid_payload = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
        }

    def test_register_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('data', response.data)
        self.assertIn('tokens', response.data['data'])
        self.assertIn('access', response.data['data']['tokens'])
        self.assertIn('refresh', response.data['data']['tokens'])

    def test_register_duplicate_email(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_register_missing_fields(self):
        response = self.client.post(self.register_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data['data'])

    def test_login_invalid_credentials(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'email': 'nobody@example.com',
            'password': 'somepass',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access_blocked(self):
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_is_hashed(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        from .models import CustomUser
        user = CustomUser.objects.get(email='test@example.com')
        self.assertNotEqual(user.password, 'testpass123')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
