from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    # path('users/signup/', views.SignUpView.as_view(),name='signup'), # サインアップ
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]