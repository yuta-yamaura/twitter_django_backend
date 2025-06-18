from django.db import models
from users.models import User

# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="followings" ,on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.follower.username

    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["follower", "following"],
                    name="follow_unique"
                )
            ]
