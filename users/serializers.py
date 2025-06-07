from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from typing import Any
from .base_serializers import BaseUserSerializer
from tweets.serializers import ProfileTweetSerializer
from .models import User

class UserSerializerWithToken(BaseUserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BaseUserSerializer.Meta.model
        fields = BaseUserSerializer.Meta.fields + ['token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserProfileSerializer(BaseUserSerializer):
    tweets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['tweets']

    def get_tweets(self, obj):
        # ユーザーのツイートを取得（作成日時の降順）
        user_tweets = obj.tweets.all().order_by('-created_at')
        print('user_tweetsの中身', user_tweets)
        user_tweets_list = ProfileTweetSerializer(user_tweets, many=True, context=self.context).data
        print('user_tweets_listの中身', user_tweets_list)
        return user_tweets_list

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tweets'] = self.get_tweets(instance)
        return data

class UpdateUserProfileSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
