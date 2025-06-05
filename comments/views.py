from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from .serializers import CommentSerializer
from .models import Comment
from tweets.models import Tweet

# Create your views here.
class TweetCommentViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     tweet_id = self.kwargs["tweet_id"]
    #     return Comment.objects.filter(tweet_id=tweet_id).order_by("-created_at")
    
    def perform_create(self, serializer):
        tweet_id = self.kwargs["tweet_id"]
        tweet = get_object_or_404(Tweet, id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)
