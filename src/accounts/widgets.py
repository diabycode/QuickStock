from django import forms
from django.contrib.auth.models import Permission

from accounts.utils import get_perm_verbose_name


class PermissionSelectWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', Permission.objects.none())
        super().__init__(*args, **kwargs)
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        label = get_perm_verbose_name(Permission.objects.get(pk=str(value)))
        return super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
