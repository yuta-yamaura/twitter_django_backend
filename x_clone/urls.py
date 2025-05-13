from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('users/register/', views.registerUser ,name='register'), # ユーザー作成
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]