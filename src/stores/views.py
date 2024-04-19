from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.sessions.models import Session

from stores.models import Store


class StoreListView(ListView):
    model = Store
    context_object_name = "store_list"
    template_name = "store/store_list.html"


class StoreCreateView(CreateView):
    model = Store
    template_name = "stores/store_create.html"
    fields = [
        "name",
        "address"
    ]
    success_url = reverse_lazy("stores:store_list")
    

class StoreUpdateView(UpdateView):
    model = Store
    template_name = "stores/store_update.html"
    fields = [
        "name",
        "address"
    ]
    success_url = reverse_lazy("stores:store_list")


class StoreDeleteView(DeleteView):
    model = Store
    template_name = "stores/store_delete.html"
    success_url = reverse_lazy("stores:store_list")


def change_store(request, pk):
    # current_store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))
    # print("current :", current_store)
    object = get_object_or_404(Store, pk=pk)
    request.session["current_store_pk"] = object.pk
    return redirect("products:product_list")