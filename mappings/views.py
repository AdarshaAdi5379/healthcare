from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from config.utils import ResponseMixin, success_response
from .models import Mapping
from .serializers import MappingSerializer
from patients.models import Patient
from doctors.serializers import DoctorSerializer


class MappingViewSet(ResponseMixin, viewsets.ModelViewSet):
    queryset = Mapping.objects.select_related('patient', 'doctor', 'assigned_by').all()
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


@extend_schema(
    responses={200: OpenApiResponse(description='Doctors assigned to patient')},
)
class PatientDoctorsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, patient_id=None):
        patient = get_object_or_404(Patient, id=patient_id)
        mappings = Mapping.objects.filter(patient=patient).select_related('doctor')
        doctors = [m.doctor for m in mappings]
        serializer = DoctorSerializer(doctors, many=True)
        return success_response(
            f'Doctors assigned to {patient.name}',
            {'patient_id': patient.id, 'patient_name': patient.name, 'doctors': serializer.data}
        )
