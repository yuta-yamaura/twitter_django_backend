from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from typing import Any
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        data["username"] = self.user.username
        data["email"] = self.user.email

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    user = User.objects.create_user(
        username = data['username'],
        email = data['email'],
        telephone_number = data['telephone_number'],
        password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)