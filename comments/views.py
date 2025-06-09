from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer, ProfileSerializer
from .models import Comment
from tweets.models import Tweet
from users.models import User
from .permissions import CommentCreateOrDelete
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, pk):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserProfileComment(generics.RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request):
        user = self.get_object()
        serializer = ProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)
