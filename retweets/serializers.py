from rest_framework import serializers
from .models import Retweet
from users.base_serializers import BaseUserSerializer

class RetweetSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Retweet
        fields = ['id', 'user', 'retweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
