import datetime

from django.forms import BaseModelForm
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from unidecode import unidecode
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.http import HttpRequest

from .models import Order, OrderStatus
from stores.models import Store
from stores.mixins import NotCurrentStoreMixin
from products.models import Product
from quickstockapp.views import get_current_period, get_period_list
from accounts.utils import log_user_action
from accounts.mixins import MyPermissionRequiredMixin
from accounts.decorators import permission_required


class OrderListView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, ListView):

    model = Order
    context_object_name = "orders"
    template_name = "orders/order_list.html"
    permission_required = "orders.can_view_order"

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
        order_list = Order.objects.filter(store=store).order_by("-add_at")

        # actual period
        now_period = {
            "month": datetime.datetime.now().month, 
            "year": datetime.datetime.now().year}

        # period filters
        periods = get_period_list(model=Order, date_field="order_date")
        selected_month, selected_year = None, None
        self.request, current_period = get_current_period(request=self.request, period_list=periods)
        if current_period:
            selected_month, selected_year = current_period.split("-")
        order_list = order_list.filter(order_date__month=selected_month, order_date__year=selected_year)

        # search query filters
        isfilters = False
        search_query = self.request.GET.get("q", None)
        if search_query:
            isfilters = True
            def func(o):
                return unidecode(search_query).lower() in o.product.unaccent_name.lower()
            order_list = filter(func, order_list)

        context["order_column_names"] = order_column_names
        context["order_list"] = order_list
        context["page_title"] = "Commandes"
        context["periods"] = periods
        context["now_period"] = now_period
        context["current_month"] = int(selected_month) if selected_month is not None else selected_month
        context["current_year"] = int(selected_year) if selected_year is not None else selected_year
        context["isfilters"] = isfilters
        if search_query:
            context["search_query"] = search_query 
        return context


class OrderDetailsView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DetailView):

    model = Order
    template_name = "orders/order_details.html"
    context_object_name = "order"
    extra_context = {"page_title": "Commandes"}
    permission_required = "orders.can_view_order"


class OrderUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, UpdateView):
    model = Order
    fields = [
        'product', # locked
        'order_date',
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
    extra_context = {"page_title": "Commandes"}
    permission_required = "orders.can_change_order"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        obj = self.get_object()
        if obj.status != OrderStatus.IN_PROGRESS:
            form.fields["status"].disabled = True
        form.fields["product"].disabled = True
        form.fields["quantity"].disabled = True
        form.fields["store"].disabled = True
        return form
    
    def form_valid(self, form):
        if not form.is_valid():
            return self.form_invalid(form)

        order_date: datetime.date = form.cleaned_data.get("order_date")
        now_date = datetime.datetime.now().date()
        if order_date > now_date:
            form.add_error("order_date", "Erreur de date")
            return self.form_invalid(form=form)

        # Check all locked fields
        locked_fields = [
            (field_name, field) for (field_name, field) in form.fields.items() 
            if field.disabled == True
        ]
        for field_name, field in locked_fields:
            if field_name in form.changed_data:
                # Return a bad request
                return HttpResponseBadRequest("Erreur: Le champ '{}' ne doit être changé.".format(field.label))
        
        form_valid_response = super().form_valid(form)
        if self.request.POST.get("add_to_stock") == "on":
            from orders.signals import order_shipped_signal
            order_shipped_signal.send(sender=Order, instance=form.instance)

        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=CHANGE,
            change_message="Commande modifié"
        ) 
        return form_valid_response

    def get_success_url(self) -> str:
        return reverse("orders:order_details", kwargs={"pk": self.kwargs.get("pk")})


class OrderCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, CreateView):
    model = Order
    fields = [
        'product',
        'order_date',
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
    extra_context = {"page_title": "Commandes"}
    permission_required = "orders.can_add_order"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        order_date: datetime.date = form.cleaned_data.get("order_date")
        now_date = datetime.datetime.now().date()
        if order_date > now_date:
            form.add_error("order_date", "Erreur de date")
            return self.form_invalid(form=form)
        
        form_valid_response = super().form_valid(form)

        if self.request.POST.get("add_to_stock") == "on":
            from orders.signals import order_shipped_signal
            order_shipped_signal.send(sender=Order, instance=form.instance)

        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=ADDITION,
            change_message="Commande ajouté"
        ) 
        return form_valid_response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        current_store = self.request.session.get("current_store_pk", None)
        from stores.models import Store
        if current_store:
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)
        store = get_object_or_404(Store, pk=current_store)
        form.fields["product"].queryset = Product.objects.filter(store=store)
        form.fields["store"].disabled = True
        return form


class OrderDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")
    extra_context = {"page_title": "Commandes"}
    permission_required = "orders.can_delete_order"

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != "2":
            return HttpResponseBadRequest("Bad request")
        log_user_action(
            user=self.request.user,
            obj=self.get_object(),
            action_flag=DELETION,
            change_message="Commande supprimé"
        ) 
        return super().post(request=request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@permission_required("orders.can_change_order")
def cancel_order(request: HttpRequest, pk):
    context = {}
    obj = get_object_or_404(Order, pk=pk)
    old_status = obj.status

    if request.method == "POST":
        obj.status = OrderStatus.CANCELLED
        obj.save()

        if request.POST.get("withdraw_from_stock") == "on":
            from orders.signals import order_cancelled_signal
            try:
                order_cancelled_signal.send(Order, instance=obj)
            except ValueError:
                obj.status = old_status
                obj.save()
                messages.error(request, "Impossible d'annuler cette commande", extra_tags="message")
                return redirect(reverse("orders:order_details", kwargs={"pk": obj.pk}))

        log_user_action(
            user=request.user,
            obj=obj,
            action_flag=CHANGE,
            change_message="Commande annulé"
        ) 
        return redirect(reverse("orders:order_details", kwargs={"pk": obj.pk}))
    context["order"] = obj
    return render(request, "orders/order_cancel.html", context)





