from django.contrib import admin

from stores.models import Store


@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
