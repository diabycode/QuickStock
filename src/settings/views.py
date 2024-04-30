from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from settings.models import EditableSettings


class SettingsUpdate(UpdateView):
    model = EditableSettings
    fields = [
        "company_name",
        "pin_code"
    ]
    template_name = "settings/update.html"
    success_url = reverse_lazy("settings:setting_update")
    
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["page_title"] = "Paramètres"
        return context

    def get_object(self, *args, **kwargs) -> Model:
        return EditableSettings.load()