from django.contrib import admin

from settings.models import EditableSettings


@admin.register(EditableSettings)
class SettingsModelAdmin(admin.ModelAdmin):
    list_display = ("company_name", "pin_code")

