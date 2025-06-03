from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializerWithToken, UserProfileSerializer, UpdateUserProfileSerializer
from django.shortcuts import get_object_or_404
from tweets.models import Tweet
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

class UserUpdateView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # シリアライザの作成
        serializer = UpdateUserProfileSerializer(instance=user, data=request.data, partial=True, many=False, context={'request': request})
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # DB更新
        serializer.save()

        return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTweet(rewuest, pk):
    tweet = Tweet.user.get(pk=pk)
    tweet.delete()
    return Response('Tweet Deleted')
