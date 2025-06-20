from django.contrib import admin
from follows.models import Follow

# Register your models here.
class Followadmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('follower', 'following')
    list_display = ('id', 'follower', 'following', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Follow, Followadmin)
