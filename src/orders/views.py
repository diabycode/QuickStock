from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Order


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    context_object_name = "orders"
    template_name = "orders/order_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        order_column_names = [
            "provider_name",
            "provider_phone",
            "order_date",
            "arrived_date",
            "description",
        ]
        
        order_list = []
        for order in Order.objects.all():
            order_list.append([
                order.provider_name,
                order.provider_phone,
                order.order_date,
                order.arrived_date,
                order.description,
            ])

        context["order_column_names"] = order_column_names
        context["order_list"] = order_list
        return context



class OrderDetailsView(LoginRequiredMixin, DetailView):

    model = Order
    template_name = "orders/order_details.html"
    context_object_name = "order"


class OrderUpdateView(LoginRequiredMixin, UpdateView):

    model = Order
    fields = [
        'provider_name',
        'provider_phone',
        'arrived_date',
        'description']
    template_name = "orders/order_update.html"



class OrderCreateView(LoginRequiredMixin, CreateView):

    model = Order
    fields = [
        'provider_name',
        'provider_phone',
        'arrived_date',
        'description']
    template_name = "orders/order_create.html"


class OrderDeleteView(DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")








