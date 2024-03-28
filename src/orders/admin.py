from django.contrib import admin

from .models import Order


@admin.register(Order)
class UserModelAdmin(admin.ModelAdmin):
    
    list_display = (
        'provider_name',
        'provider_phone',
        'order_date',
        'arrived_date',
        'description',
    )

