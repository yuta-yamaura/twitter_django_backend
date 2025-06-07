from django.contrib import admin
from .models import Comment

# Register your models here.
class CommentsModeladmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('user', 'tweet', 'comment', 'image')
    list_display = ('id', 'user', 'tweet', 'comment', 'image', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Comment, CommentsModeladmin)
