from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Bookmark
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import BookmarkSerializer, BookmarkListSerializer

# Create your views here.
class BookmarkToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, tweet=tweet)
        if created:
            serializer = BookmarkSerializer(bookmark)
            return Response({
                "message": "ブックマークしました",
                "bookmark": serializer.data
            })
        else:
            return Response({"detail": "すでに「ブックマーク」済みです"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            tweet = Tweet.objects.get(pk=pk)
            like = Bookmark.objects.get(user=request.user, tweet=tweet)
            like.delete()
            return Response({
                "message": "ブックマークを削除しました"
            }, status=status.HTTP_200_OK)
        except Tweet.DoesNotExist:
            return Response({"message": "ツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        except Bookmark.DoesNotExist:
            return Response({"message": "ブックマークしたツイートが存在しません"}, status=status.HTTP_404_NOT_FOUND)
        
class BookmarkList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.pk)
        serializer = BookmarkListSerializer(user, many=False, context={"request": request})
        return Response(serializer.data)
