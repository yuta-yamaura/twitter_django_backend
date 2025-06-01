from rest_framework import serializers
from .models import User

class BaseUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
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
            'name',
            'self_introduction',
            'background_image',
            'created_at',
            'isAdmin'
        ]

    def get__id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.username

    def get_isAdmin(self, obj):
        return obj.is_staff 
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'id': data['id'],
            'username': data['username'],
            'email': data['email'],
            'image': data['image'],
            'accountName': data['account_name'],
            'name': data['name'],
            'selfIntroduction': data['self_introduction'],
            'backgroundImage': data['background_image'],
            'createdAt': data['created_at'],
        }