from rest_framework import serializers
from .models import Comment
from tweets.models import Tweet
from users.base_serializers import BaseUserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'contents', 'comments', 'image', 'created_at']
        read_only_fields = ['user', 'contents', 'created_at']
