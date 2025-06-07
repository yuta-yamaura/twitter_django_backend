from rest_framework import serializers
from .models import Tweet
from users.base_serializers import BaseUserSerializer

class TweetSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'image', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at']
