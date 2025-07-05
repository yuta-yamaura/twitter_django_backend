from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Bookmark
from .serializers import BookmarkSerializer, BookmarkTweetSerializer
from django.db.models import OuterRef, Count, Exists

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
        
class BookmarkListAPIView(generics.ListAPIView):
    serializer_class = BookmarkTweetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        user_retweets = user.retweets.filter(tweet=OuterRef('pk'))
        user_likes = user.likes.filter(tweet=OuterRef('pk'))
        
        return Tweet.objects.filter(
                bookmarks__user=user
            ).annotate(
                retweet_count=Count('retweets', distinct=True),
                like_count=Count('likes', distinct=True),
                login_user_retweeted=Exists(user_retweets),
                login_user_liked=Exists(user_likes)
            ).select_related('user').order_by('-created_at')
