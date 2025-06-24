from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = None  # ページネーションを無効にする

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, is_read=False).order_by("-created_at")
