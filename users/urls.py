from django.urls import path
from . import views
from .serializers import MyTokenObtainPairView

urlpatterns = [
    path('register/', views.registerUser, name='register'), # ユーザー作成
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
