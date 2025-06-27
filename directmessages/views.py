from django.shortcuts import render
from rest_framework import viewsets
from .models import DirectMessageRoom, DirectMessageUser, DirectMessage
from .serializers import DirectMessageUserSerializer, ChatHistorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.db.models import Q, Max, Subquery, OuterRef

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
            # exists_group = DirectMessageUser.objects.filter(user=sender_user)
            # if exists_group:
            #     return Response(None)
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

    # TODO:複数回クエリを実行してるので、最適化する必要がある
    def list(self, request):
        message_groups = DirectMessageUser.objects.filter(
            user=self.request.user
            ).values_list('room', flat=True)
        group_list = DirectMessageUser.objects.filter(room__in=message_groups).exclude(user=self.request.user).values_list('user', flat=True)
        user_group_list = DirectMessageUser.objects.filter(user__in=group_list)
        serializer = DirectMessageUserSerializer(user_group_list, many=True, context={'request': request})
        return Response(serializer.data)

class ChatHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    queryset = DirectMessage.objects.all()
    permission_classes = [IsAuthenticated]
    
    def list(self, request, sender_id=None, recipient_name=None):
        recipient = User.objects.get(username=recipient_name)
        chat_history = DirectMessage.objects.filter(
            Q(sender=sender_id, recipient=recipient) | Q(sender=recipient, recipient=sender_id)
        ).order_by("created_at")
        serializer = ChatHistorySerializer(chat_history, many=True)
        return Response(serializer.data)
