from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from users.models import User
from .models import DirectMessage

class WebChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *atgs, **kwargs):
        super().__init__(*atgs, **kwargs)
        self.room_name = "testserver"
        self.user = None

    def connect(self):
        self.accept()
        # 送信者と受信者のkeyを取得
        self.sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        self.recipient_name = self.scope["url_route"]["kwargs"]["recipient_name"]
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def receive_json(self, content):
        recipient = User.objects.get(username=self.recipient_name)
        sender = User.objects.get(pk=self.sender_id)
        message = content["message"]
        new_message = DirectMessage.objects.create(sender=sender, recipient=recipient, content=message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "chat.message",
                "new_message": {
                    "sender": new_message.sender.username,
                    "recipient": new_message.recipient.username,
                    "content": new_message.content,
                    "created_at": new_message.created_at.isoformat(timespec='minutes')
                }
            },
        )
    
    def chat_message(self, event):
        self.send_json(event)

    def disconnect(self, close_code):
        pass
