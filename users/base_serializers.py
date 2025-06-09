from rest_framework import serializers
from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'image',
            'account_name',
            'self_introduction',
            'background_image',
            'address',
            'date_of_birth',
            'web_site',
            'created_at',
        ]
