from django.db import models
from users.models import User

# Create your models here.
class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_dms', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_dms', on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
