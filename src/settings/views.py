from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from settings.models import EditableSettings
from settings.forms import SettingsModelfForm


class SettingsUpdate(LoginRequiredMixin, UpdateView):
    model = EditableSettings
    form_class = SettingsModelfForm
    template_name = "settings/update.html"
    success_url = reverse_lazy("settings:setting_update")
    
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["page_title"] = "Paramètres"
        return context
    
    def get_form(self, form_class=None) -> BaseModelForm:
        form = super().get_form(form_class)
        return form 

    def get_object(self, *args, **kwargs) -> Model:
        return EditableSettings.load()
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            password = form.cleaned_data.get("password_confirm")
            if password:
                if self.request.user.check_password(password):
                    messages.success(self.request, "Enregistré avec succès", extra_tags="message")
                    return super().form_valid(form)
                else:
                    from django.forms.utils import ErrorList
                    errors = form._errors.setdefault("password_confirm", ErrorList())
                    errors.append("Mot de passe incorrect")
                    return self.form_invalid(form=form)
                    