from rest_framework import viewsets
from .models import DirectMessageRoom, DirectMessageUser, DirectMessage
from .serializers import DirectMessageUserSerializer, ChatHistorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User

# Create your views here.
class MessageGroupCreate(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # URLパラメータからuser_idを取得
        recipient_user_id = self.kwargs['user_id']
        sender_user = self.request.user
        
        try:
            recipient_user = User.objects.get(id=recipient_user_id)
            # 既存のDMグループがあれば何も返さない
            message_groups = DirectMessageUser.objects.filter(user=self.request.user).values_list('room', flat=True)
            exists_group_list = DirectMessageUser.objects.filter(room__in=message_groups).exclude(user=self.request.user)
            if exists_group_list:
                return Response(None)
            # DMグループ作成
            room = DirectMessageRoom.objects.create()
            direct_message_user = [
                DirectMessageUser(user=recipient_user, room=room),
                DirectMessageUser(user=sender_user, room=room)
            ]
            DirectMessageUser.objects.bulk_create(
                direct_message_user
            )
            
            sender_group = DirectMessageUser.objects.get(user=sender_user, room=room)
            serializer = DirectMessageUserSerializer(sender_group, context={'request': request})
            return Response(serializer.data)
            
        except User.DoesNotExist:
            return Response({'error': 'ユーザーが見つかりません'}, status=404)
        except Exception as e:
            print('エラー:', e)
            return Response({'error': str(e)}, status=500)

class MessageGroup(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    queryset = DirectMessageUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self, *args, **kwatgs):
        context = super().get_serializer_context(*args, **kwatgs)
        context["request"] = self.request
        return context

    def list(self, request):
        message_groups = DirectMessageUser.objects.filter(user=self.request.user).values_list('room', flat=True)
        user_group_list = DirectMessageUser.objects.filter(room__in=message_groups).exclude(user=self.request.user).order_by("-created_at")
        serializer = DirectMessageUserSerializer(user_group_list, many=True, context={'request': request})
        return Response(serializer.data)

class ChatHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    queryset = DirectMessage.objects.all()
    permission_classes = [IsAuthenticated]
    
    def list(self, request, username=None):
        recipient = User.objects.get(username=username)
        # 送信者と受信者が合致するルームインスタンスを取得
        sender_rooms = DirectMessageUser.objects.filter(user=self.request.user).values_list("room", flat=True)
        recipient_rooms = DirectMessageUser.objects.filter(user=recipient).values_list("room", flat=True)
        room_id = sender_rooms.intersection(recipient_rooms).get()
        chat_history = DirectMessage.objects.filter(room=room_id).order_by("created_at")
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data)
