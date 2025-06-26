from django.contrib import admin
from .models import Bookmark

# Register your models here.
class Bookmarkadmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('user', 'tweets')
    list_display = ('id', 'user', 'tweets', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Bookmark, Bookmarkadmin)
