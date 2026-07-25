from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'email', 'contact_number',
                  'experience', 'available_from', 'available_to',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError('Experience cannot be negative')
        return value

    def validate_email(self, value):
        if Doctor.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('A doctor with this email already exists')
        return value
