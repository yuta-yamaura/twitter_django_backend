from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.registerUser ,name='register'), # ユーザー作成
]