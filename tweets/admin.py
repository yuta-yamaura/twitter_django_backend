from django.contrib import admin
from .models import Tweet

# Register your models here.
class Tweetsadmin(admin.ModelAdmin):
    list_editable = ('content',)
    fields = ('user', 'content', 'image')
    list_display = ('id', 'user', 'image', 'content', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Tweet, Tweetsadmin)
