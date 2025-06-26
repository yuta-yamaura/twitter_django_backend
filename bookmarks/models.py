from django.db import models
from users.models import User
from tweets.models import Tweet

# Create your models here.
class Bookmark(models.Model):
    user = models.ForeignKey(User, related_name="bookmarks", on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="bookmarks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
