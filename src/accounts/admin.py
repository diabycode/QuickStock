from django.contrib import admin

from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'email', 'first_name', 'last_name')

