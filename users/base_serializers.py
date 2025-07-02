from rest_framework import serializers
from .models import User
from django.conf import settings

class BaseUserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    background_image = serializers.SerializerMethodField()
    
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
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_background_image(self, obj):
        if obj.background_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.background_image.url)
            return obj.background_image.url
        return None
