from django.urls import path
from . import views
from .views import TweetCommentViewSet, CommentDestroy, UserProfileComment

urlpatterns = [
    path('tweets/<int:tweet_id>/comments/', TweetCommentViewSet.as_view(), name='tweet_comments_list_create'),
    path('comments/<int:pk>/', CommentDestroy.as_view(), name='tweet_comments_delete'),
    path('user/<int:pk>/comments/', UserProfileComment.as_view(), name='user_comments_list'),
]
