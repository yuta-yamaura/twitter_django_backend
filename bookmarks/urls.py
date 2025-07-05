from django.urls import path
from .views import BookmarkToggleAPIView, BookmarkListAPIView

urlpatterns = [
    path('tweets/<int:pk>/bookmark/', BookmarkToggleAPIView.as_view(), name='tweet_bookmark'),
    path('tweets/<int:pk>/unbookmark/', BookmarkToggleAPIView.as_view(), name='tweet_bookmark'),
    path('bookmark/', BookmarkListAPIView.as_view(), name='bookmark_list'),
]
