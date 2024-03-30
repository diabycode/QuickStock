from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .models import Product


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        product_column_names = []
        product_list = []
        for product in Product.objects.all():
            if not product_column_names:
                product_column_names.extend([
                    "#",
                    Product.name.field.verbose_name,
                    Product.stock_quantity.field.verbose_name,
                    Product.wholesale_unit_price.field.verbose_name + " (FCFA)",
                    Product.unit_price_sale.field.verbose_name + " (FCFA)",
                    Product.packaging_type.field.verbose_name,
                ])
            product_list.append([
                product.pk,
                product.name,
                product.stock_quantity,
                product.wholesale_unit_price,
                product.unit_price_sale,
                product.packaging_type,
            ])

        context["product_column_names"] = product_column_names
        context["product_list"] = Product.objects.all()
        return context


class ProductDetailsView(LoginRequiredMixin, DetailView):

    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"


class ProductUpdateView(LoginRequiredMixin, UpdateView):

    model = Product
    fields = [
        'name',
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
        'stock_quantity',
        'wholesale_unit_price',
        'unit_price_sale',
        'packaging_type']
    template_name = "products/product_create.html"
    success_url = reverse_lazy("products:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("products:product_list")




