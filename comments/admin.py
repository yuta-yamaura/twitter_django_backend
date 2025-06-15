from django.contrib import admin
from .models import Comment

# Register your models here.
class CommentsModeladmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('user', 'tweet', 'content', 'image')
    list_display = ('id', 'user', 'tweet', 'content', 'image', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Comment, CommentsModeladmin)
