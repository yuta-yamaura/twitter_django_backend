from django.urls import path
from . import views
from .views import TweetCommentViewSet

urlpatterns = [
    path('tweets/<int:tweet_id>/comments/', TweetCommentViewSet.as_view(), name='tweet_comments_list_create'),
]
