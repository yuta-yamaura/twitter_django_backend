from django.contrib import admin
from .models import Like

# Register your models here.
class Likesdmin(admin.ModelAdmin):
    list_editable = ()
    fields = ('user', 'tweet')
    list_display = ('id', 'user', 'tweet', 'created_at', 'updated_at')
    list_display_links = None

admin.site.register(Like, Likesdmin)
