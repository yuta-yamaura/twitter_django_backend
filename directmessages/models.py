from django.db import models
from users.models import User

# Create your models here.
class DirectMessageRoom(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DirectMessageUser(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    room = models.ForeignKey(DirectMessageRoom, related_name='rooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "room"],
                name="room_unique"
            )
        ]

class DirectMessage(models.Model):
    room = models.ForeignKey(DirectMessageRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='senders', on_delete=models.CASCADE)
    content = models.TextField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
