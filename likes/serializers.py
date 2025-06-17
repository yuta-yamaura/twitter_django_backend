from rest_framework import serializers
from .models import Like
from users.base_serializers import BaseUserSerializer
from rest_framework.response import Response
from users.models import User
from django.db.models import Count
from tweets.models import Tweet

class LikeSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProfileNiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tweet = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at', 'like_count', 'retweet_count']
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
    
    def get_tweet(self, obj):
        # プロフィール画面に必要なツイート情報を取得
        return {
            'image': self.get_tweet_image(obj),
            'content': obj.content
        }

    def get_tweet_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProfileSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['like']

    def get_like(self, obj):
        liked_tweet_ids = Like.objects.filter(user=obj.pk).values_list('tweet_id', flat=True)
        user_liked_tweets = Tweet.objects.filter(id__in=liked_tweet_ids).annotate(like_count=Count('likes', distinct=True), retweet_count=Count('retweets', distinct=True)).order_by('-created_at')
        user_liked_tweets_list = ProfileNiceSerializer(user_liked_tweets, many=True, context=self.context).data
        return user_liked_tweets_list
