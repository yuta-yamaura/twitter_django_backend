from rest_framework import serializers
from .models import Comment
from tweets.models import Tweet
from users.models import User
from users.base_serializers import BaseUserSerializer
from rest_framework.response import Response

class CommentSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment', 'image', 'created_at']
        read_only_fields = ['user', 'tweet', 'created_at']

class ProfileCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'comment', 'image', 'created_at']
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

class ProfileSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ['comments']

    def get_comments(self, obj):
        # ユーザーのコメントを取得（作成日時の降順）
        user_comments = obj.user_comments.all().order_by('-created_at')
        user_comments_list = ProfileCommentSerializer(user_comments, many=True, context=self.context).data
        print('user_comments_listの中身', user_comments_list)
        return user_comments_list
