from django.urls import path
from .views import LikeToggleAPIView, ProfileLike

urlpatterns = [
    path('tweets/<int:pk>/like/', LikeToggleAPIView.as_view(), name='tweet_like'),
    path('tweets/<int:pk>/unlike/', LikeToggleAPIView.as_view(), name='tweet_unlike'),
    path('user/<int:pk>/like/', ProfileLike.as_view(), name='profile_retweet_list'),
]
