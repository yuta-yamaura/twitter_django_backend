from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatHistoryViewSet, MessageGroup, MessageGroupCreate

router = DefaultRouter()
router.register(r'directmessages', ChatHistoryViewSet, basename='directmessages')

urlpatterns = [
    path('', include(router.urls)),
    # メッセージグループ作成エンドポイント
    path('message-group-create/<int:user_id>/', MessageGroupCreate.as_view({'post': 'create'}), name='message_group_create'),
    path('message-group/', MessageGroup.as_view({'get': 'list'}), name='message_group'),
    # チャット履歴を取得するための専用エンドポイント
    path('chat-history/<str:username>/', ChatHistoryViewSet.as_view({'get': 'list'}), name='chat_history'),
]
