from django.urls import path
from . import views
from .views import TweetCommentViewSet, CommentDestroy

urlpatterns = [
    path('tweets/<int:tweet_id>/comments/', TweetCommentViewSet.as_view(), name='tweet_comments_list_create'),
    path('comments/<str:pk>/', CommentDestroy.as_view(), name='tweet_comments_delete'),
    # path('comments/<str:pk>/', views.delete_comment, name='tweet_comments_delete'),
]
