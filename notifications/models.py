from django.db import models
from users.models import User

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('LK','like'),
        ('FL','follow'),
        ('CM','comment'),
        ('RT','retweet'),
    )

    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES, default=None)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient.username
