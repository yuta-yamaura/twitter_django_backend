from rest_framework import serializers
from .models import Notification
from users.base_serializers import BaseUserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    sender = BaseUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'recipient', 'sender', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'notification_type', 'recipient', 'sender', 'message', 'is_read', 'created_at', 'updated_at']
