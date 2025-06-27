from rest_framework import serializers
from .models import DirectMessageUser
from users.base_serializers import BaseUserSerializer

class DirectMessageUserSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = DirectMessageUser
        fields = ['id', 'user', 'room', 'created_at', 'updated_at']

class ChatHistorySerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = DirectMessageUser
        fields = ['id', 'user', 'room', 'created_at', 'updated_at']
