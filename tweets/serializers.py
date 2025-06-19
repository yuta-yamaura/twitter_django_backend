from rest_framework import serializers
from .models import Tweet
from users.base_serializers import BaseUserSerializer

class TweetSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    login_user_retweeted = serializers.BooleanField(read_only=True)
    login_user_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'image', 'created_at', 'user', 'retweet_count', 'like_count', 'login_user_retweeted', 'login_user_liked']
        read_only_fields = ['id', 'created_at', 'updated_at', 'retweet_count', 'like_count', 'login_user_retweeted', 'login_user_liked']

class ProfileTweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'image', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        # プロフィール画面に必要なユーザー情報を取得
        return {
            'image': self.get_user_image(obj)
        }
    
    def get_user_image(self, obj):
        if obj.user.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.image.url)
            return obj.user.image.url
        return None

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
