from django.db import models
from users.models import User

# Create your models here.
class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_message(from_user, to_user, content):
        sender_message = DirectMessage(
            sender=from_user,
            recipient=to_user,
            content=content
        )
        sender_message.save()
        return sender_message

    # @classmethod
    # def get_inbox(cls, users):
    #     message_sender = DirectMessage.objects.filter(Q(recipient=users) | Q(sender=users)).order_by('-created_at')
    #     messages = User.objects.prefetch_related(
    #         Prefetch(
    #             'from_user',
    #             queryset = message_sender
    #         )
    #     ).filter((Q(pk__in=message_sender.values('sender')) | Q(pk__in=message_sender.values('recipient'))) & ~Q(pk=users.pk)).annotate(last=Max('created_at'))
    #     return messages