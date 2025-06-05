from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Tweet
from .serializers import TweetSerializer
from .permissions import CreateUserEditOrDelete
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by("-created_at")
    serializer_class = TweetSerializer
    # 第三者が他のTweetを編集、削除できないようカスタムパーミッションを指定
    permission_classes = [CreateUserEditOrDelete]

    def perform_create(self, serializer):
        # 新規作成時に "user" を自動的にセット
        serializer.save(user=self.request.user)
