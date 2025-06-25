from django.shortcuts import render
from rest_framework import viewsets
from .models import DirectMessage
from .serializers import ChatHistorySerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from django.db.models import Q, Max, Subquery, OuterRef

# Create your views here.
class MessageGroupCreate(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # URLパラメータからrecipient_idを取得
        recipient_id = self.kwargs['recipient_id']
        
        try:
            recipient = User.objects.get(id=recipient_id)
            # 既存のDMグループがあれば何も返さない
            exists_group = DirectMessage.objects.filter(sender=request.user, recipient=recipient)
            if exists_group:
                return Response(None)
            # DMグループ作成
            group = DirectMessage.objects.create(
                sender=request.user, 
                recipient=recipient,
                content=None  # 空のメッセージ
            )
            
            serializer = ChatHistorySerializer(group, context={'request': request})
            return Response(serializer.data)
            
        except User.DoesNotExist:
            return Response({'error': 'ユーザーが見つかりません'}, status=404)
        except Exception as e:
            print('エラー:', e)
            return Response({'error': str(e)}, status=500)

class MessageGroup(viewsets.ModelViewSet):
    serializer_class = ChatHistorySerializer
    queryset = DirectMessage.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self, *args, **kwatgs):
        context = super().get_serializer_context(*args, **kwatgs)
        context["request"] = self.request
        return context

    def list(self, request):
        latest_message = DirectMessage.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
            ).filter(
                created_at=Subquery(
                    DirectMessage.objects.filter(
                        Q(sender=OuterRef('sender'), recipient=OuterRef('recipient')) |
                        Q(sender=OuterRef('recipient'), recipient=OuterRef('sender'))
                    ).values('created_at').order_by('-created_at')[:1]
                )
            )
        serializer = ChatHistorySerializer(latest_message, many=True, context={'request': request})
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
