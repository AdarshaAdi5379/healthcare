from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'contact_number', 'address',
                  'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError('Age must be between 0 and 150')
        return value

    def validate_contact_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError(
                'Contact number must be at least 10 digits'
            )
        return value

    def validate_gender(self, value):
        if value not in dict(Patient.GENDER_CHOICES):
            raise serializers.ValidationError('Invalid gender choice')
        return value
