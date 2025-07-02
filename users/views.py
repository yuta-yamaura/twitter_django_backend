from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User
from .serializers import UserSerializerWithToken, UserProfileSerializer, UpdateOrDeleteUserSerializer
from django.shortcuts import get_object_or_404
from tweets.models import Tweet
from .permissions import UserProfileEdit, UserAccountDelete
from django.db.models import Exists, OuterRef
from follows.models import Follow
from django.core.exceptions import PermissionDenied
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

class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [UserProfileEdit]
    serializer_class = UpdateOrDeleteUserSerializer
    queryset = User.objects.all()

    def get_object(self):
        login_user = self.request.user
        is_login_user_subquery = User.objects.filter(pk=OuterRef('pk'), id=login_user.id)
        follow_status = Follow.objects.values_list('follower', flat=True).filter(following=self.kwargs["pk"])
        obj = User.objects.annotate(login_user=Exists(is_login_user_subquery), following=Exists(follow_status)).get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        # GETリクエストとPATCHリクエストで異なるシリアライザーを使用
        if self.request.method == 'PATCH':
            return UpdateOrDeleteUserSerializer
        return UserProfileSerializer

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [UserAccountDelete]
    serializer_class = UpdateOrDeleteUserSerializer

    def get_object(self):
        try:
            delete_user = self.request.user
            self.check_object_permissions(self.request, delete_user)
            return delete_user
        except PermissionDenied:
            message = {'detail': 'ユーザー削除の権限がありません'}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
