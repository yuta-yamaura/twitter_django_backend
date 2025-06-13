from django.urls import path
from . import views
from .views import RetweetToggleAPIView

urlpatterns = [
    path('tweets/<int:pk>/retweet/', RetweetToggleAPIView.as_view(), name='tweet_like'),
    path('tweets/<int:pk>/unretweet/', RetweetToggleAPIView.as_view(), name='tweet_unlike'),
]
