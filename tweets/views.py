from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer
from .permissions import CreateUserEditOrDelete

# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by("-created_at")
    serializer_class = TweetSerializer
    # 第三者が他のTweetを編集、削除できないようカスタムパーミッションを指定
    permission_classes = [CreateUserEditOrDelete]

    def perform_create(self, serializer):
        # 新規作成時に "user" を自動的にセット
        serializer.save(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTweet(rewuest, pk):
    tweet = Tweet.user.get(pk=pk)
    tweet.delete()
    return Response('Tweet Deleted')
