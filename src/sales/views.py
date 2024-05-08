import datetime

from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.forms.utils import ErrorList
from django.http import HttpRequest, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from unidecode import unidecode

from .models import Sale, SaleStatus
from stores.models import Store
from stores.mixins import NotCurrentStoreMixin
from products.models import Product
from quickstockapp.views import get_period_list, get_current_period


class SaleListView(LoginRequiredMixin, NotCurrentStoreMixin, ListView):

    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        sale_column_names = [
            Sale.sale_date.field.verbose_name,
            Sale.status.field.verbose_name,
            Sale.product.field.verbose_name,
            Sale.quantity.field.verbose_name,
            Sale.buyer_name.field.verbose_name,
            Sale.buyer_phone.field.verbose_name,
        ]
        
        store = get_object_or_404(Store, pk=self.request.session.get("current_store_pk"))
        sale_list = Sale.objects.filter(store=store).order_by("sale_date")
        
        # periods
        now_period = {
            "month": datetime.datetime.now().month, 
            "year": datetime.datetime.now().year}

        # period filters
        periods = get_period_list(model=Sale, date_field="sale_date")
        selected_month, selected_year = None, None
        self.request, current_period = get_current_period(request=self.request, period_list=periods)
        if current_period:
            selected_month, selected_year = current_period.split("-")
        
        sale_list = sale_list.filter(sale_date__month=selected_month, sale_date__year=selected_year)
        
        # search query filters
        isfilters = False
        search_query = self.request.GET.get("q", None)
        if search_query:
            isfilters = True
            def func(s):
                return unidecode(search_query).lower() in s.product.unaccent_name.lower()
            sale_list = filter(func, sale_list)

        context["sale_column_names"] = sale_column_names
        context["sale_list"] = sale_list
        context["page_title"] = "Ventes"
        context["periods"] = periods
        context["now_period"] = now_period
        context["current_month"] = int(selected_month) if selected_month is not None else selected_month
        context["current_year"] = int(selected_year) if selected_year is not None else selected_year
        context["isfilters"] = isfilters
        if search_query:
            context["search_query"] = search_query 
        return context


class SaleDetailsView(LoginRequiredMixin, NotCurrentStoreMixin, DetailView):
    model = Sale
    template_name = "sales/sale_details.html"
    context_object_name = "sale"


class SaleCreateView(LoginRequiredMixin, NotCurrentStoreMixin, CreateView):

    model = Sale
    fields = [
        'sale_date',
        'product',
        'store',
        'quantity',
        'buyer_name',
        'buyer_phone',
    ]
    template_name = "sales/sale_create.html"
    success_url = reverse_lazy("sales:sale_list")

    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            form_data = form.cleaned_data

            if form_data.get("status") == SaleStatus.CANCELLED:
                return HttpResponseBadRequest("bad request")

            if form_data.get("quantity") > form_data.get("product").stock_quantity:
                quantity_errors = form._errors.setdefault("quantity", ErrorList())
                quantity_errors.append("Le stock produit est insufisant")
                return self.form_invalid(form=form)

        return super().form_valid(form) 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        current_store = self.request.session.get("current_store_pk", None)
        from stores.models import Store
        if current_store:
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)

        store = get_object_or_404(Store, pk=current_store)
        form.fields["product"].queryset = Product.objects.filter(store=store)
        return form


class SaleUpdateView(LoginRequiredMixin, NotCurrentStoreMixin, UpdateView):
    model = Sale
    fields = [
        'sale_date',
        'product', # locked
        'store', 
        'quantity', # locked
        'buyer_name',
        'buyer_phone',
    ]
    template_name = "sales/sale_update.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["product"].disabled = True
        form.fields["quantity"].disabled = True
        # form.fields["status"].disabled = True
        return form
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # verif if locked fields got changes
        locked_fields = [
            (field_name, field) for (field_name, field) in form.fields.items() 
            if field.disabled == True
        ]
        for field_name, field in locked_fields:
            if field_name in form.changed_data:
                return HttpResponseBadRequest("Erreur: Le champ '{}' ne doit être changé.".format(field.label))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("sales:sale_details", kwargs={"pk": self.kwargs.get("pk")})


class SaleDeleteView(LoginRequiredMixin, NotCurrentStoreMixin, DeleteView):
    model = Sale
    context_object_name = "sale"
    template_name = "sales/sale_delete.html"
    success_url = reverse_lazy("sales:sale_list")

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != "2":
            return HttpResponseBadRequest("Bad request")
        return super().post(request=request, *args, **kwargs)

@login_required(login_url='/accounts/login/')
def cancel_sale(request, pk):
    if request.method == "POST":
        obj = get_object_or_404(Sale, pk=pk)
        old_status = obj.status
        obj.status = SaleStatus.CANCELLED

        try:
            obj.save(forced_save=True)
        except ValueError:
            messages.error(request, "Impossible d'annuler cette vente", extra_tags="message")
            return redirect(reverse("sales:sale_details", kwargs={"pk": obj.pk}))
        
        if old_status != SaleStatus.CANCELLED:
            try:
                # sale cancel signal
                from products.signals import update_quantity_on_sale_cancellation
                from sales.signals import sale_cancelled_signal
                sale_cancelled_signal.send(update_quantity_on_sale_cancellation, instance=obj)
            except:
                obj.status = old_status
                obj.save()
                messages.error(request, "Impossible d'annuler cette vente", extra_tags="message")
                return redirect(reverse("sales:sale_details", kwargs={"pk": obj.pk}))
        return redirect(reverse("sales:sale_details", kwargs={"pk": obj.pk}))
    return HttpResponseBadRequest("Bad request")


