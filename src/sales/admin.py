from django.contrib import admin

from .models import Sale

@admin.register(Sale)
class SaleModelAdmin(admin.ModelAdmin):
    
    list_display = (
        'sale_date',
        'product',
        'quantity',
        'buyer_name',
        'buyer_phone'
    )


