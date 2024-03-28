from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"


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






