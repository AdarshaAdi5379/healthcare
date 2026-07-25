from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Patient
from accounts.models import CustomUser


class PatientTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create_user(
            email='user1@test.com', name='User One', password='pass1234'
        )
        self.user2 = CustomUser.objects.create_user(
            email='user2@test.com', name='User Two', password='pass1234'
        )
        self.client.force_authenticate(user=self.user1)
        self.valid_payload = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'M',
            'contact_number': '9876543210',
            'address': '123 Main St',
        }

    def test_create_patient(self):
        response = self.client.post('/api/patients/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'John Doe')
        self.assertEqual(Patient.objects.count(), 1)

    def test_create_patient_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/patients/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_own_patients(self):
        self.client.post('/api/patients/', self.valid_payload, format='json')
        self.client.force_authenticate(user=self.user2)
        self.client.post('/api/patients/', {
            'name': 'Jane Doe', 'age': 25, 'gender': 'F',
            'contact_number': '5555555555'
        }, format='json')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/patients/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['created_by'], self.user1.id)

    def test_cannot_access_other_users_patient(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.post('/api/patients/', self.valid_payload, format='json')
        patient_id = resp.data['data']['id']
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/patients/{patient_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_patient(self):
        resp = self.client.post('/api/patients/', self.valid_payload, format='json')
        patient_id = resp.data['data']['id']
        response = self.client.put(
            f'/api/patients/{patient_id}/',
            {'name': 'John Updated', 'age': 31, 'gender': 'M', 'contact_number': '9876543210'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'John Updated')

    def test_cannot_update_other_users_patient(self):
        resp = self.client.post('/api/patients/', self.valid_payload, format='json')
        patient_id = resp.data['data']['id']
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(
            f'/api/patients/{patient_id}/',
            {'name': 'Hacked', 'age': 99, 'gender': 'M', 'contact_number': '9876543210'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_patient(self):
        resp = self.client.post('/api/patients/', self.valid_payload, format='json')
        patient_id = resp.data['data']['id']
        response = self.client.delete(f'/api/patients/{patient_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    def test_cannot_delete_other_users_patient(self):
        resp = self.client.post('/api/patients/', self.valid_payload, format='json')
        patient_id = resp.data['data']['id']
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/patients/{patient_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_negative_age_rejected(self):
        payload = {**self.valid_payload, 'age': -5}
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_age_above_150_rejected(self):
        payload = {**self.valid_payload, 'age': 200}
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_phone_rejected(self):
        payload = {**self.valid_payload, 'contact_number': '123'}
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_name_rejected(self):
        payload = {**self.valid_payload, 'name': ''}
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_gender_rejected(self):
        payload = {**self.valid_payload, 'gender': 'X'}
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_created_by_set_automatically(self):
        response = self.client.post('/api/patients/', self.valid_payload, format='json')
        self.assertEqual(response.data['data']['created_by'], self.user1.id)
