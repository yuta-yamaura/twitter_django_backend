from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']
        read_only_fields = ['created_at']
