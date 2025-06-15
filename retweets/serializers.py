from rest_framework import serializers
from .models import Retweet
from users.base_serializers import BaseUserSerializer
from rest_framework.response import Response
from users.models import User

class RetweetSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Retweet
        fields = ['id', 'user', 'retweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProfileRetweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tweet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Retweet
        fields = ['id', 'user', 'tweet', 'retweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        # プロフィール画面に必要なユーザー情報を取得
        return {
            'image': self.get_user_image(obj)
        }
    
    def get_user_image(self, obj):
        if obj.retweet.user.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.retweet.user.image.url)
            return obj.retweet.user.image.url
        return None
    
    def get_tweet(self, obj):
        # プロフィール画面に必要なツイート情報を取得
        return {
            'image': self.get_tweet_image(obj),
            'content': obj.retweet.content
        }

    def get_tweet_image(self, obj):
        if obj.retweet.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.retweet.image.url)
            return obj.retweet.image.url
        return None

class ProfileSerializer(serializers.ModelSerializer):
    retweet = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['retweet']

    def get_retweet(self, obj):
        user_retweet = obj.user_retweets.all().order_by('-created_at')
        user_retweet_list = ProfileRetweetSerializer(user_retweet, many=True, context=self.context).data
        return user_retweet_list
