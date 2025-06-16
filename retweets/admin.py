from django.contrib import admin
from .models import Retweet

# Register your models here.
class Retweetsadmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('user', 'tweet')
    list_display = ('id', 'user', 'tweet', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Retweet, Retweetsadmin)
