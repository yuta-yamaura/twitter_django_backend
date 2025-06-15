from django.urls import path
from . import views
from .views import RetweetToggleAPIView, ProfileRetweet

urlpatterns = [
    path('tweets/<int:pk>/retweet/', RetweetToggleAPIView.as_view(), name='tweet_like'),
    path('tweets/<int:pk>/unretweet/', RetweetToggleAPIView.as_view(), name='tweet_unlike'),
    path('user/<int:pk>/retweet/', ProfileRetweet.as_view(), name='profile_retweet_list'),
]
