from rest_framework import serializers
from .models import DirectMessage
from users.base_serializers import BaseUserSerializer

class ChatHistorySerializer(serializers.ModelSerializer):
    sender = BaseUserSerializer(read_only=True)
    recipient = BaseUserSerializer(read_only=True)

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'recipient', 'content', 'created_at', 'updated_at']
