from rest_framework import serializers
from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            '_id',
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
            'isAdmin'
        ]

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff 
