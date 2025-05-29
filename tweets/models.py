from django.db import models
from users.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, related_name="tweets" ,on_delete=models.CASCADE)
    content = models.CharField(max_length=140, null=True, blank=True)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
