from rest_framework import viewsets, permissions
from .models import Doctor
from .serializers import DoctorSerializer
from config.utils import ResponseMixin


class DoctorViewSet(ResponseMixin, viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
