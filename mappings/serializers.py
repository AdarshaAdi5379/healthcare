from rest_framework import serializers
from .models import Mapping
from patients.models import Patient
from doctors.serializers import DoctorSerializer


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    class Meta:
        model = Mapping
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name',
                  'doctor_specialization', 'assigned_by', 'assigned_at']
        read_only_fields = ['id', 'assigned_by', 'assigned_at']

    def validate(self, data):
        if Mapping.objects.filter(
            patient=data['patient'], doctor=data['doctor']
        ).exists():
            raise serializers.ValidationError(
                'This patient is already assigned to this doctor'
            )
        return data


class PatientDoctorsSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    doctors = DoctorSerializer(many=True)
