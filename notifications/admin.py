from django.contrib import admin
from .models import Notification

# Register your models here.
class Notificationadmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('notification_type', 'recipient', 'sender', 'message', 'is_read')
    list_display = ('id', 'notification_type', 'recipient', 'sender', 'message', 'is_read', 'created_at')
    list_display_links = None

admin.site.register(Notification, Notificationadmin)
