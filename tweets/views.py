from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer
from .permissions import TweetDeletePermission, CreateUserEditOrDelete
from django.db.models import Count, Exists, OuterRef
from retweets.models import Retweet
# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    # queryset = 
    serializer_class = TweetSerializer
    # 第三者が他のTweetを編集、削除できないようデフォルトのパーミッションにカスタムパーミッションを指定
    permission_classes = [CreateUserEditOrDelete]

    # destroyメソッドの場合のみTweetDeletePermissionを設定
    def get_permissions(self):
        if self.action == 'destroy':
            return [TweetDeletePermission()]
        return [CreateUserEditOrDelete()]

    def perform_create(self, serializer):
        # 新規作成時に "user" を自動的にセット
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # has_object_permissionメソッドを呼び出す
            self.check_object_permissions(instance, request)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise exceptions.AuthenticationFailed('このツイートを削除する権限がありません')

    def get_queryset(self):
        if self.action == 'list':
            # OuterRefでTweetモデルのpkとRetweetモデルのretweetカラムを比較
            user_retweet = Retweet.objects.filter(user=self.request.user, retweet=OuterRef('pk'))
            tweet_list = Tweet.objects.all().annotate(retweet_count=Count('tweet_retweets'), login_user_retweeted=Exists(user_retweet)).order_by("-created_at")
            return tweet_list
        if self.action == 'retrieve':
            tweet = Tweet.objects.get(pk = self.kwargs["pk"])
            retweet_tweet = tweet.tweet_retweets.filter(user = self.request.user)
            retweet = Tweet.objects.annotate(retweet_count=Count('tweet_retweets'), login_user_retweeted=Exists(retweet_tweet)).order_by("-created_at")
            return retweet
