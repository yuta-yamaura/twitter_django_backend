from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import FollowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Follow
from rest_framework import status
from notifications.models import Notification

# Create your views here.
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, pk):
        follow_user = self.request.user
        following_user = User.objects.get(pk=self.kwargs["pk"])
        following, created = Follow.objects.get_or_create(following=following_user, follower=follow_user)
        if created:
            serializer = FollowSerializer(following)
            Notification.objects.create(
                notification_type = 'FL',
                recipient = following_user,
                sender = request.user,
                message = f"{request.user.username}があなたをフォローしました"
            )
            return Response({
                "message": "フォローしました",
                "follow": serializer.data
            })
        else:
            return Response({"detail": "すでにフォロー済みです"}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            follow_user = self.request.user
            following_user = User.objects.get(pk=self.kwargs["pk"])
            following = Follow.objects.get(following=following_user ,follower=follow_user)
            following.delete()
            return Response({
                "message": "フォローを解除しました"
            }, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({
                "message": "フォローしたアカウントが見つかりませんでした"
            }, status=status.HTTP_404_NOT_FOUND)
