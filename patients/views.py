from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from .models import Patient
from .serializers import PatientSerializer
from .permissions import IsOwner
from config.utils import ResponseMixin


class PatientViewSet(ResponseMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
