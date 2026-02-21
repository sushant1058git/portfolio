from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError('Name must be at least 2 characters.')
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError('Message must be at least 20 characters.')
        return value.strip()
