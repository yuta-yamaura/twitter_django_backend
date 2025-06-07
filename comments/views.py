from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from .serializers import CommentSerializer
from .models import Comment
from tweets.models import Tweet
from users.models import User
from .permissions import CommentCreateOrDelete
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# Create your views here.
class TweetCommentViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentCreateOrDelete]

    def get_queryset(self):
        tweet_id = self.kwargs["tweet_id"]
        return Comment.objects.filter(tweet_id=tweet_id).order_by("-created_at")
    
    def perform_create(self, serializer):
        tweet_id = self.kwargs["tweet_id"]
        tweet = get_object_or_404(Tweet, id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)

class CommentDestroy(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentCreateOrDelete]

    def get_object(self):
        obj = get_object_or_404(Comment, pk=self.kwargs["pk"])
        print('viewsのobjの中身', obj)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, pk):
        print('requestの中身', request)
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
