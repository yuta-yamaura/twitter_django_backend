from rest_framework import serializers
from .models import Like
from users.base_serializers import BaseUserSerializer
from rest_framework.response import Response
from users.models import User

class LikeSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProfileNiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tweet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        # プロフィール画面に必要なユーザー情報を取得
        return {
            'image': self.get_user_image(obj)
        }
    
    def get_user_image(self, obj):
        if obj.tweet.user.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.tweet.user.image.url)
            return obj.tweet.user.image.url
        return None
    
    def get_tweet(self, obj):
        # プロフィール画面に必要なツイート情報を取得
        return {
            'image': self.get_tweet_image(obj),
            'content': obj.tweet.content
        }

    def get_tweet_image(self, obj):
        if obj.tweet.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.tweet.image.url)
            return obj.tweet.image.url
        return None

class ProfileSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['like']

    def get_like(self, obj):
        user_like = obj.user_likes.all().order_by('-created_at')
        user_like_list = ProfileNiceSerializer(user_like, many=True, context=self.context).data
        return user_like_list
