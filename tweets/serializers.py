from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    account_name = serializers.ReadOnlyField(source='user.account_name')
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'user_image', 'account_name', 'image', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'username', 'account_name']

    def get_user_image(self, obj):
        if obj.user.image:
            request = self.context.get('request')
            print(request)
            if request:
                return request.build_absolute_uri(obj.user.image.url)
            return obj.user.image.url
        return None
    
