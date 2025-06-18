from django.urls import path
from .views import FollowAPIView

urlpatterns = [
    path('users/<int:pk>/follow/', FollowAPIView.as_view(), name='follow_user'),
    path('users/<int:pk>/unfollow/', FollowAPIView.as_view(), name='unfollow_user'),
]
