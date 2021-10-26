from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        ('System credentials', {'fields': ('username', 'password', 'email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),

    )

    list_display = ['username', 'user_type', ]


admin.site.register(User, UserAdmin)
