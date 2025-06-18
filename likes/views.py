from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Like
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import ProfileSerializer, LikeSerializer

# Create your views here.
class LikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tweet, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if created:
            serializer = LikeSerializer(tweet)
            return Response({
                "message": "いいねしました",
                "retweet": serializer.data
            })
        else:
            return Response({"detail": "すでに「いいね」済みです"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
            like = Like.objects.get(user=request.user, tweet=tweet)
            like.delete()
            return Response({
                "message": "いいねを削除しました"
            }, status=status.HTTP_200_OK)
        except Tweet.DoesNotExist:
            return Response({"message": "ツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        except Like.DoesNotExist:
            return Response({"message": "いいねしたツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        
class ProfileLike(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        serializer = ProfileSerializer(user, many=False, context={"request": request})
        return Response(serializer.data)
