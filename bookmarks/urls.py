from django.urls import path
from .views import BookmarkToggleAPIView, BookmarkList

urlpatterns = [
    path('tweets/<int:pk>/bookmark/', BookmarkToggleAPIView.as_view(), name='tweet_bookmark'),
    path('tweets/<int:pk>/unbookmark/', BookmarkToggleAPIView.as_view(), name='tweet_bookmark'),
    path('<int:pk>/bookmark/', BookmarkList.as_view(), name='bookmark_list'),
]
