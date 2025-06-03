from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'username']
