from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.sessions.models import Session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied

from stores.mixins import NotCurrentStoreMixin
from stores.models import Store, StoreCategory
from accounts.mixins import MyPermissionRequiredMixin
from accounts.decorators import permission_required


class StoreListView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, ListView):
    model = Store
    context_object_name = "store_list"
    template_name = "store/store_list.html"
    permission_required = "stores.can_view_store"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        """
        store_categories = [
            {
                'category_name': '...',
                'store_list': [
                    store...
                ]
            }, ...
        ]
        for category in store_categories:
            show : category.category_name
            for store in category.store_list:
                show : store
        """
        store_categories = []
        category_list = StoreCategory.choices
        if self.request.user.has_perm("stores.can_access_all_store"):
            for category in category_list:
                store_categories.append({
                    "category_name": category[1],
                    "store_list": Store.objects.filter(category=category[0])
                })
        else:
            for category in category_list:
                store_categories.append({
                    "category_name": category[1],
                    "store_list": Store.objects.filter(category=category[0], users__in=[self.request.user])
                })

        store_categories = list(sorted(store_categories, key=lambda c: c["category_name"]))
        context["store_categories"] = store_categories
        return context


class StoreCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, CreateView):
    model = Store
    template_name = "stores/store_create.html"
    fields = [
        "name",
        "address",
        "category",
        "accent_color_code",
        "users",
        "description",
    ]
    success_url = reverse_lazy("stores:store_list")
    permission_required = "stores.can_add_store"
    

class StoreUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, UpdateView):
    model = Store
    template_name = "stores/store_update.html"
    fields = [
        "name",
        "address",
        "category",
        "accent_color_code",
        "users",
        "description",
    ]
    success_url = reverse_lazy("stores:store_list")
    permission_required = "stores.can_change_store"


class StoreDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, DeleteView):
    model = Store
    template_name = "stores/store_delete.html"
    success_url = reverse_lazy("stores:store_list")
    permission_required = "stores.can_delete_store"


@login_required(login_url="/accounts/login/")
def change_store(request: HttpRequest, pk):
    object: Store = get_object_or_404(Store, pk=pk)
    if request.user.has_perm("stores.can_access_all_store") or request.user in object.users.all():
        request.session["current_store_pk"] = object.pk
        return redirect("accounts:details")
    raise PermissionDenied("Accès interdit !")
