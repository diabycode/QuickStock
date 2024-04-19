from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from .models import Order, OrderStatus
from stores.models import Store


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    context_object_name = "orders"
    template_name = "orders/order_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        order_column_names = [
            Order.order_date.field.verbose_name ,
            Order.status.field.verbose_name,
            Order.product.field.verbose_name,
            Order.quantity.field.verbose_name,
            Order.arrived_date.field.verbose_name,
            Order.provider_name.field.verbose_name,
            Order.shipping_costs.field.verbose_name + " (FCFA)",
        ]

        store = get_object_or_404(Store, pk=self.request.session.get("current_store_pk"))
        
        context["order_column_names"] = order_column_names
        context["order_list"] = Order.objects.filter(store=store).order_by("order_date")
        context["page_title"] = "Commandes"
        return context


class OrderDetailsView(LoginRequiredMixin, DetailView):

    model = Order
    template_name = "orders/order_details.html"
    context_object_name = "order"


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = [
        'product', # locked
        'quantity', # locked
        'store', 
        'provider_name', 
        'provider_phone',
        'status', # locked if not in progress
        'arrived_date',
        'shipping_costs',
        'description',
    ]
    template_name = "orders/order_update.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        obj = self.get_object()
        if obj.status != OrderStatus.IN_PROGRESS:
            form.fields["status"].disabled = True
        form.fields["product"].disabled = True
        form.fields["quantity"].disabled = True
        return form
    
    def form_valid(self, form):
        
        # Check all locked fields
        locked_fields = [
            (field_name, field) for (field_name, field) in form.fields.items() 
            if field.disabled == True
        ]
        for field_name, field in locked_fields:
            if field_name in form.changed_data:
                # Return a bad request
                return HttpResponseBadRequest("Erreur: Le champ '{}' ne doit être changé.".format(field.label))
        
        obj = self.get_object()
        old_status = obj.status
        form_status_value = form.cleaned_data.get("status")
        
        if old_status == OrderStatus.IN_PROGRESS and form_status_value != old_status:
            if form_status_value == OrderStatus.SHIPPED:
                # order cancellation signal
                from products.signals import update_quantity_on_order_shipped
                from orders.signals import order_shipped_signal
                order_shipped_signal.send(update_quantity_on_order_shipped, instance=obj)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("orders:order_details", kwargs={"pk": self.kwargs.get("pk")})


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = [
        'product',
        'quantity',
        'store',
        'provider_name',
        'provider_phone',
        'status',
        'arrived_date',
        'shipping_costs',
        'description',
    ]
    template_name = "orders/order_create.html"
    success_url = reverse_lazy("orders:order_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        current_store = self.request.session.get("current_store_pk", None)
        if current_store:
            from stores.models import Store
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)
        # print(dir(form.fields["store"]))
        return form


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != "2":
            return HttpResponseBadRequest("Bad request")
        return super().post(request=request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def cancel_order(request, pk):
    if request.method == "POST":
        obj = get_object_or_404(Order, pk=pk)
        old_status = obj.status
        obj.status = OrderStatus.CANCELLED
        obj.save()

        if old_status != OrderStatus.CANCELLED and old_status != OrderStatus.IN_PROGRESS:
            # order cancellation signal
            from products.signals import update_quantity_on_order_cancelled
            from orders.signals import order_cancelled_signal
            order_cancelled_signal.send(update_quantity_on_order_cancelled, instance=obj)
        return HttpResponse("Commande annulé avec succès.")
    return HttpResponseBadRequest("Bad request")





