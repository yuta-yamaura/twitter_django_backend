from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializerWithToken
# Create your views here.

@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            telephone_number=data['telephoneNumber'],
            password=data['password']
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data['token'])
    except:
        message = {'ユーザー登録に失敗しました。'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
