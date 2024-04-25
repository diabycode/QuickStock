from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.sessions.models import Session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from stores.models import Store


class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    context_object_name = "store_list"
    template_name = "store/store_list.html"


class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    template_name = "stores/store_create.html"
    fields = [
        "name",
        "address"
    ]
    success_url = reverse_lazy("stores:store_list")
    

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    template_name = "stores/store_update.html"
    fields = [
        "name",
        "address"
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
    return redirect("products:product_list")