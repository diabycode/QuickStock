from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .models import Product
from stores.models import Store


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        product_column_names = [
            Product.name.field.verbose_name,
            Product.stock_quantity.field.verbose_name,
            Product.wholesale_unit_price.field.verbose_name + " (FCFA)",
            Product.unit_price_sale.field.verbose_name + " (FCFA)",
            Product.packaging_type.field.verbose_name,
        ]
        
        store = get_object_or_404(Store, pk=self.request.session.get("current_store_pk"))

        context["product_column_names"] = product_column_names
        context["product_list"] = Product.objects.filter(store=store).order_by("-pk")
        context["page_title"] = "Produits"
        return context


class ProductDetailsView(LoginRequiredMixin, DetailView):

    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"


class ProductUpdateView(LoginRequiredMixin, UpdateView):

    model = Product
    fields = [
        'name',
        'store',
        'stock_quantity',
        'wholesale_unit_price',
        'unit_price_sale',
        'packaging_type']
    template_name = "products/product_update.html"
    
    def get_success_url(self) -> str:
        return reverse("products:product_details", kwargs={"slug": self.kwargs.get("slug")})


class ProductCreateView(LoginRequiredMixin, CreateView):

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        current_store = self.request.session.get("current_store_pk", None)
        if current_store:
            from stores.models import Store
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)
        # print(dir(form.fields["store"]))
        return form 


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("products:product_list")




