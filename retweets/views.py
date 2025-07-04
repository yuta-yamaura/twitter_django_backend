from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Retweet
from .serializers import RetweetSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import ProfileSerializer
from notifications.models import Notification

# Create your views here.
class RetweetToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        retweet, created = Retweet.objects.get_or_create(user=request.user, tweet=tweet)
        if created:
            serializer = RetweetSerializer(retweet)
            Notification.objects.create(
                notification_type = 'RT',
                recipient = tweet.user,
                sender = request.user,
                message = f"{request.user.username}があなたのツイートをリツイートしました"
            )
            return Response({
                "message": "リツイートを作成しました",
                "retweet": serializer.data
            })
        else:
            return Response({"detail": "すでにリツイート済みです"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
            retweet = Retweet.objects.get(user=request.user, tweet=tweet)
            retweet.delete()
            return Response({
                "message": "リツイートを削除しました"
            }, status=status.HTTP_200_OK)
        except Tweet.DoesNotExist:
            return Response({"message": "ツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        except Retweet.DoesNotExist:
            return Response({"message": "リツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        
class ProfileRetweet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        serializer = ProfileSerializer(user, many=False, context={"request": request})
        return Response(serializer.data)
