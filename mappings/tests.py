from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Mapping
from patients.models import Patient
from doctors.models import Doctor
from accounts.models import CustomUser


class MappingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='mapper@test.com', name='Mapper', password='pass1234'
        )
        self.client.force_authenticate(user=self.user)
        self.patient = Patient.objects.create(
            name='Test Patient', age=30, gender='M',
            contact_number='1111111111', created_by=self.user
        )
        self.doctor = Doctor.objects.create(
            name='Test Doctor', specialization='General',
            email='doctor@test.com', contact_number='2222222222'
        )
        self.valid_payload = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
        }

    def test_create_mapping(self):
        response = self.client.post('/api/mappings/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mapping.objects.count(), 1)

    def test_create_mapping_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/mappings/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_mapping_rejected(self):
        self.client.post('/api/mappings/', self.valid_payload, format='json')
        response = self.client.post('/api/mappings/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_mappings(self):
        self.client.post('/api/mappings/', self.valid_payload, format='json')
        response = self.client.get('/api/mappings/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['patient_name'], 'Test Patient')
        self.assertEqual(response.data[0]['doctor_name'], 'Test Doctor')

    def test_get_doctors_by_patient(self):
        self.client.post('/api/mappings/', self.valid_payload, format='json')
        response = self.client.get(f'/api/mappings/by-patient/{self.patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['patient_name'], 'Test Patient')
        self.assertEqual(len(response.data['data']['doctors']), 1)
        self.assertEqual(response.data['data']['doctors'][0]['name'], 'Test Doctor')

    def test_get_doctors_by_patient_no_mappings(self):
        response = self.client.get(f'/api/mappings/by-patient/{self.patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['doctors']), 0)

    def test_delete_mapping(self):
        resp = self.client.post('/api/mappings/', self.valid_payload, format='json')
        mapping_id = resp.data['data']['id']
        response = self.client.delete(f'/api/mappings/{mapping_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mapping.objects.count(), 0)

    def test_invalid_patient_rejected(self):
        payload = {'patient': 9999, 'doctor': self.doctor.id}
        response = self.client.post('/api/mappings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_doctor_rejected(self):
        payload = {'patient': self.patient.id, 'doctor': 9999}
        response = self.client.post('/api/mappings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
