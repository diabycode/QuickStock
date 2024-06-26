from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.sessions.models import Session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from stores.mixins import NotCurrentStoreMixin
from stores.models import Store, StoreCategory


class StoreListView(LoginRequiredMixin, NotCurrentStoreMixin, ListView):
    model = Store
    context_object_name = "store_list"
    template_name = "store/store_list.html"

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
        for category in category_list:
            store_categories.append({
                "category_name": category[1],
                "store_list": Store.objects.filter(category=category[0])
            })
        store_categories = list(sorted(store_categories, key=lambda c: c["category_name"]))
        context["store_categories"] = store_categories
        return context


class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    template_name = "stores/store_create.html"
    fields = [
        "name",
        "address",
        "category",
        "accent_color_code",
    ]
    success_url = reverse_lazy("stores:store_list")
    

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    template_name = "stores/store_update.html"
    fields = [
        "name",
        "address",
        "category",
        "accent_color_code"
    ]
    success_url = reverse_lazy("stores:store_list")


class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Store
    template_name = "stores/store_delete.html"
    success_url = reverse_lazy("stores:store_list")


@login_required(login_url="/accounts/login/")
def change_store(request, pk):
    # current_store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))
    # print("current :", current_store)
    object = get_object_or_404(Store, pk=pk)
    request.session["current_store_pk"] = object.pk
    return redirect("home")