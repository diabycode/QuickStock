import datetime

from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from unidecode import unidecode

from .models import Product
from stores.models import Store
from stores.mixins import NotCurrentStoreMixin
from sales.models import Sale
from quickstockapp.views import get_period_list, get_current_period
from accounts.utils import log_user_action
from accounts.mixins import MyPermissionRequiredMixin


class ProductListView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    permission_required = "products.can_view_product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        product_column_names = [
            Product.name.field.verbose_name,
            Product.stock_quantity.field.verbose_name,
            Product.unit_price_sale.field.verbose_name + " (FCFA)",
            Product.store.field.verbose_name,
            Product.add_at.field.verbose_name,
        ]
        try:
            store = Store.objects.get(pk=self.request.session.get("current_store_pk"))
        except Store.DoesNotExist:
            store = Store.objects.first()
            if store:
                self.request.session["current_store_pk"] = store.pk

        products_list = Product.objects.filter(store=store).order_by("-pk")

        isfilters = False

        # filters
        search_query = self.request.GET.get("q", None)
        if search_query:
            isfilters = True
            def func(p):
                return unidecode(search_query).lower() in p.unaccent_name.lower()
            products_list = filter(func, products_list)

        context["product_column_names"] = product_column_names
        context["product_list"] = products_list
        context["page_title"] = "Produits & Stock"
        context["isfilters"] = isfilters
        if search_query:
            context["search_query"] = search_query 
        return context


class ProductDetailsView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DetailView):

    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"
    permission_required = "products.can_view_product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        obj: Product = self.get_object()
        sale_column_names = [
            Sale.sale_date.field.verbose_name,
            Sale.status.field.verbose_name,
            "Qté",
            Sale.store.field.verbose_name,
            Sale.seller.field.verbose_name,
            # Sale.quantity.field.verbose_name,
        ]

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
        
        context["recent_sales"] = obj.get_recent_sales(month=selected_month, year=selected_year)
        context["sale_column_names"] = sale_column_names
        context["now_period"] = now_period
        context["periods"] = periods
        context["page_title"] = "Produits & Stock"
        context["current_month"] = int(selected_month) if selected_month is not None else selected_month
        context["current_year"] = int(selected_year) if selected_year is not None else selected_year

        return context


class ProductUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, UpdateView):

    model = Product
    fields = [
        'name',
        'store',
        'stock_quantity',
        'wholesale_unit_price',
        'unit_price_sale',
        'packaging_type']
    template_name = "products/product_update.html"
    extra_context = {"page_title": "Produits & Stock"}
    permission_required = "products.can_change_product"
    
    def get_success_url(self) -> str:
        return reverse("products:product_details", kwargs={"slug": self.kwargs.get("slug")})
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid_response = super().form_valid(form)
        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=CHANGE,
            change_message="Produit modifié"
        )
        return form_valid_response


class ProductCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, CreateView):

    model = Product
    fields = [
        'name',
        'store',
        'stock_quantity',
        'wholesale_unit_price',
        'unit_price_sale',
        'packaging_type']
    template_name = "products/product_create.html"
    success_url = reverse_lazy("products:product_list")
    extra_context = {"page_title": "Produits & Stock"}
    permission_required = "products.can_add_product"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        current_store = self.request.session.get("current_store_pk", None)
        if current_store:
            from stores.models import Store
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)
        # print(dir(form.fields["store"]))
        return form 

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_valid_response = super().form_valid(form)
        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=ADDITION,
            change_message="Produit ajouté"
        )
        return form_valid_response


class ProductDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("products:product_list")
    extra_context = {"page_title": "Produits & Stock"}
    permission_required = "products.can_delete_product"

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        log_user_action(
            user=self.request.user,
            obj=self.get_object(),
            action_flag=DELETION,
            change_message="Produit supprimé"
        )
        return super().post(request, *args, **kwargs)
