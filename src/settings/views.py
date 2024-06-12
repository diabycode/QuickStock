from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from settings.models import EditableSettings
from settings.forms import SettingsModelfForm
from accounts.mixins import MyPermissionRequiredMixin


class SettingsUpdate(LoginRequiredMixin, MyPermissionRequiredMixin, UpdateView):
    model = EditableSettings
    form_class = SettingsModelfForm
    template_name = "settings/update.html"
    success_url = reverse_lazy("settings:setting_update")
    permission_required = "settings.can_change_setting"
    
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["page_title"] = "Paramètres"
        context["settings_object"] = self.get_object()
        return context

    def get_object(self, *args, **kwargs) -> Model:
        return EditableSettings.load()
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            password = form.cleaned_data.get("password_confirm")
            if self.request.user.check_password(password):
                form.save()
                messages.success(self.request, "Enregistré avec succès", extra_tags="message")
                return redirect(reverse("settings:setting_update"))
            else:
                form.add_error("password_confirm", "Mot de passe incorrect")
                messages.error(self.request, "Mot de passe incorrect", extra_tags="message")
        return self.form_invalid(form=form)
    
    


