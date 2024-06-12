from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


class MyPermissionRequiredMixin(PermissionRequiredMixin):
    access_denied_url = reverse_lazy("permission_denied")
    login_url = reverse_lazy("accounts:login")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(self.access_denied_url)  