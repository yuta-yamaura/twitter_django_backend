from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializerWithToken
from django.contrib.auth.hashers import make_password
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            telephone_number=data['telephone_number'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data['token'])
    except:
        message = {'ユーザー登録に失敗しました。'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
