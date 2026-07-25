from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Doctor
from accounts.models import CustomUser


class DoctorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='doctoradmin@test.com', name='Admin', password='pass1234'
        )
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'name': 'Sarah Smith',
            'specialization': 'Cardiology',
            'email': 'sarah@hospital.com',
            'contact_number': '9988776655',
            'experience': 10,
        }

    def test_create_doctor(self):
        response = self.client.post('/api/doctors/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Sarah Smith')
        self.assertEqual(Doctor.objects.count(), 1)

    def test_create_doctor_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/doctors/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_doctors(self):
        self.client.post('/api/doctors/', self.valid_payload, format='json')
        response = self.client.get('/api/doctors/')
        self.assertEqual(len(response.data), 1)

    def test_get_doctor_detail(self):
        resp = self.client.post('/api/doctors/', self.valid_payload, format='json')
        doctor_id = resp.data['data']['id']
        response = self.client.get(f'/api/doctors/{doctor_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sarah Smith')

    def test_update_doctor(self):
        resp = self.client.post('/api/doctors/', self.valid_payload, format='json')
        doctor_id = resp.data['data']['id']
        response = self.client.put(
            f'/api/doctors/{doctor_id}/',
            {**self.valid_payload, 'name': 'Sarah Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Sarah Updated')

    def test_delete_doctor(self):
        resp = self.client.post('/api/doctors/', self.valid_payload, format='json')
        doctor_id = resp.data['data']['id']
        response = self.client.delete(f'/api/doctors/{doctor_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Doctor.objects.count(), 0)

    def test_duplicate_email_rejected(self):
        self.client.post('/api/doctors/', self.valid_payload, format='json')
        response = self.client.post('/api/doctors/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_experience_rejected(self):
        payload = {**self.valid_payload, 'experience': -1}
        response = self.client.post('/api/doctors/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_name_rejected(self):
        payload = {**self.valid_payload, 'name': ''}
        response = self.client.post('/api/doctors/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_available_time_validation(self):
        from datetime import time
        payload = {
            **self.valid_payload,
            'available_from': '14:00:00',
            'available_to': '09:00:00',
        }
        response = self.client.post('/api/doctors/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
