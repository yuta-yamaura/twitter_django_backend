from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Tweet
from .serializers import TweetSerializer

# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by("-created_at")
    serializer_class = TweetSerializer
    # 認証済みユーザーは読み書き可能、未認証ユーザーは読み取りのみ可能
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print(self.request)
        # 新規作成時に "user" を自動的にセット
        serializer.save(user=self.request.user)
