from django.db import models
from users.models import User
from tweets.models import Tweet

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments" ,on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="comments", on_delete=models.CASCADE)
    comments = models.TextField(max_length=140, null=True, blank=True)
    image = models.ImageField(upload_to='tweet_images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
