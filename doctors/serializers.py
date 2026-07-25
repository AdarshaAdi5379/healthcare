from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'email', 'contact_number',
                  'experience', 'available_from', 'available_to',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name cannot be empty')
        return value

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError('Experience cannot be negative')
        return value

    def validate_email(self, value):
        if Doctor.objects.filter(email=value).exclude(
            id=self.instance.id if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                'A doctor with this email already exists'
            )
        return value

    def validate(self, data):
        if data.get('available_from') and data.get('available_to'):
            if data['available_from'] >= data['available_to']:
                raise serializers.ValidationError(
                    'available_from must be earlier than available_to'
                )
        return data
