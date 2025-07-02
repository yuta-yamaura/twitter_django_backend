from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from users.models import User
from .models import DirectMessageUser, DirectMessage, DirectMessageRoom
from django.contrib.auth.models import AnonymousUser

class WebChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *atgs, **kwargs):
        super().__init__(*atgs, **kwargs)
        self.room_name = "testserver"
        self.user = None

    def connect(self):
        self.accept()
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            self.user = self.scope["user"]
            # 受信者のkeyを取得
            self.username = self.scope["url_route"]["kwargs"]["username"]
            recipient_user = User.objects.get(username=self.username)
            # 送信者と受信者が合致するルームインスタンスを取得
            sender_rooms = self.user.direct_message_users.values_list("room", flat=True)
            recipient_rooms = recipient_user.direct_message_users.values_list("room", flat=True)
            room_id = sender_rooms.intersection(recipient_rooms).get()
            self.room = DirectMessageRoom.objects.get(id=room_id)
            async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def receive_json(self, content):
        sender = User.objects.get(pk=self.user_id)
        message = content["content"]
        new_message = DirectMessage.objects.create(sender=sender, content=message, room=self.room)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "chat.message",
                "new_message": {
                    "sender": new_message.sender.username,
                    "content": new_message.content,
                    "room": new_message.room.id,
                    "created_at": new_message.created_at.isoformat(timespec='minutes')
                }
            },
        )
    
    def chat_message(self, event):
        self.send_json(event)

    def disconnect(self, close_code):
        pass
