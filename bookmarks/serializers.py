from rest_framework import serializers
from .models import Bookmark
from users.base_serializers import BaseUserSerializer
from rest_framework.response import Response
from users.models import User
from tweets.models import Tweet
from django.db.models import Count, OuterRef, Exists
from retweets.models import Retweet
from likes.models import Like

class BookmarkSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookmarkTweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tweet = serializers.SerializerMethodField(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    login_user_retweeted = serializers.BooleanField(read_only=True)
    login_user_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'tweet', 'created_at', 'retweet_count', 'like_count', 'login_user_retweeted', 'login_user_liked']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user(self, obj):
        # プロフィール画面に必要なユーザー情報を取得
        return {
            'image': self.get_user_image(obj),
            'account_name': obj.user.account_name,
            'username': obj.user.username
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

class BookmarkListSerializer(serializers.ModelSerializer):
    bookmark = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['bookmark']

    def get_bookmark(self, obj):
        bookmarked_tweet_ids = obj.bookmarks.values_list('tweet_id', flat=True)
        user_retweeted = obj.retweets.filter(tweet=OuterRef('pk'))
        user_liked = obj.likes.filter(tweet=OuterRef('pk'))
        user_bookmarked_tweets = Tweet.objects.filter(id__in=bookmarked_tweet_ids).annotate(retweet_count=Count('retweets', distinct=True), like_count=Count('likes', distinct=True), login_user_retweeted=Exists(user_retweeted), login_user_liked=Exists(user_liked)).order_by('-created_at')
        user_bookmarked_tweets_list = BookmarkTweetSerializer(user_bookmarked_tweets, many=True, context=self.context).data
        return user_bookmarked_tweets_list
