from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializerWithToken
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            telephone_number=data['telephone_number'],
            password=data['password']
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        print('エラーの詳細:', str(e))
        message = {'detail': 'ユーザー登録に失敗しました。'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
