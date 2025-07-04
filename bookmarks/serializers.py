from rest_framework import serializers
from .models import Bookmark
from users.base_serializers import BaseUserSerializer
from tweets.models import Tweet

class BookmarkSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookmarkTweetSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    login_user_retweeted = serializers.BooleanField(read_only=True)
    login_user_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'created_at', 'user', 'image',
                 'retweet_count', 'like_count',
                 'login_user_retweeted', 'login_user_liked']
