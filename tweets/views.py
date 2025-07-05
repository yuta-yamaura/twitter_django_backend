from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer
from .permissions import TweetDeletePermission, CreateUserEditOrDelete
from django.db.models import Count, Exists, OuterRef
from retweets.models import Retweet
from likes.models import Like
from bookmarks.models import Bookmark
# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
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
            tweet_pk = self.kwargs["pk"]
            instance = Tweet.objects.get(pk=tweet_pk)
            # has_object_permissionメソッドを呼び出す
            self.check_object_permissions(instance, request)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise exceptions.AuthenticationFailed('このツイートを削除する権限がありません')

    def get_queryset(self):
        if self.action == 'list':
            # OuterRefでTweetモデルのpkとRetweetモデルのretweetカラムを比較
            user_retweeted = Retweet.objects.filter(user=self.request.user, tweet=OuterRef('pk'))
            user_liked = Like.objects.filter(user=self.request.user, tweet=OuterRef('pk'))
            user_bookmarked = Bookmark.objects.filter(user=self.request.user, tweet=OuterRef('pk'))
            tweet_list = Tweet.objects.all().annotate(retweet_count=Count('retweets', distinct=True), like_count=Count('likes', distinct=True), login_user_retweeted=Exists(user_retweeted), login_user_liked=Exists(user_liked), login_user_bookmarked=Exists(user_bookmarked)).order_by("-created_at")
            return tweet_list
        if self.action == 'retrieve':
            tweet = Tweet.objects.get(pk = self.kwargs["pk"])
            user_retweeted = tweet.retweets.filter(user = self.request.user)
            user_liked = tweet.likes.filter(user = self.request.user)
            user_bookmarked = tweet.bookmarks.filter(user = self.request.user)
            retweet = Tweet.objects.annotate(retweet_count=Count('retweets', distinct=True), like_count=Count('likes', distinct=True), login_user_retweeted=Exists(user_retweeted), login_user_liked=Exists(user_liked), login_user_bookmarked=Exists(user_bookmarked)).order_by("-created_at")
            return retweet
