from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
    (None, {'fields': ('username', 'email', 'password', 'telephone_number', 'image', 'background_image', 'account_name', 'self_introduction', 'address', 'web_site', 'date_of_birth')}),
    (None, {'fields': ('is_active', 'is_admin',)}),
    )

    list_display = ('id', 'username', 'email', 'telephone_number', 'account_name', 'self_introduction', 'address', 'web_site', 'date_of_birth', 'image', 'background_image', 'avater', 'follow', 'info_flg', 'created_at', 'updated_at', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)