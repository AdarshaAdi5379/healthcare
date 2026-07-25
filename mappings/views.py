from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Mapping
from .serializers import MappingSerializer
from patients.models import Patient
from doctors.serializers import DoctorSerializer


class MappingViewSet(viewsets.ModelViewSet):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class PatientDoctorsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, patient_id=None):
        patient = get_object_or_404(Patient, id=patient_id)
        mappings = Mapping.objects.filter(patient=patient)
        doctors = [m.doctor for m in mappings]
        serializer = DoctorSerializer(doctors, many=True)
        return Response({
            'patient_id': patient.id,
            'patient_name': patient.name,
            'doctors': serializer.data
        })
