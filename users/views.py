from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import User
from .serializers import UserSerializerWithToken, UserProfileSerializer, UpdateUserProfileSerializer
from django.shortcuts import get_object_or_404
from tweets.models import Tweet
from .permissions import UserProfileEdit
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
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
        return Response(serializer.data)
    except Exception as e:
        print('エラーの詳細:', str(e))
        message = {'detail': 'ユーザー登録に失敗しました。'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [UserProfileEdit]
    serializer_class = UpdateUserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        user = self.get_object()
        serializer = UserProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTweet(rewuest, pk):
    tweet = Tweet.user.get(pk=pk)
    tweet.delete()
    return Response('Tweet Deleted')
