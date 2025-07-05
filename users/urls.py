from django.urls import path
from . import views
from .serializers import MyTokenObtainPairView

urlpatterns = [
    path('register/', views.registerUser, name='register'), # ユーザー作成
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('info/', views.UserInfo.as_view(), name='info'), # ホーム画面のユーザー情報取得
    path('profile/<int:pk>/', views.UserUpdateView.as_view(), name='user-profile'),
    path('delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
