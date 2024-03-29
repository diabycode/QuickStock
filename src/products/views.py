from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Product


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        product_column_names = [
            "name",
            "stock_quantity",
            "packaging_type",
        ]
        product_list = []
        for product in Product.objects.all():
            product_list.append([
                product.name,
                product.stock_quantity,
                product.packaging_type,
            ])

        context["product_column_names"] = product_column_names
        context["product_list"] = product_list
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
        'packaging_type']
    template_name = "products/product_update.html"



class ProductCreateView(LoginRequiredMixin, CreateView):

    model = Product
    fields = [
        'name',
        'stock_quantity',
        'packaging_type']
    template_name = "products/product_create.html"


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("products:product_list")




