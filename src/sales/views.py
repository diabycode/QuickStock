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

from .models import Sale, SaleStatus


class SaleListView(LoginRequiredMixin, ListView):

    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        sale_column_names = [
            "#",
            Sale.sale_date.field.verbose_name,
            Sale.status.field.verbose_name,
            Sale.product.field.verbose_name,
            Sale.quantity.field.verbose_name,
            Sale.buyer_name.field.verbose_name,
            Sale.buyer_phone.field.verbose_name,
        ]
        
        context["sale_column_names"] = sale_column_names
        context["sale_list"] = Sale.objects.all()
        return context


class SaleDetailsView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sales/sale_details.html"
    context_object_name = "sale"


class SaleCreateView(LoginRequiredMixin, CreateView):

    model = Sale
    fields = [
        'sale_date',
        'product',
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


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = Sale
    fields = [
        'sale_date',
        'product', # locked
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


class SaleDeleteView(LoginRequiredMixin, DeleteView):
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
        obj.save()

        if old_status != SaleStatus.CANCELLED:
            # sale cancel signal
            from products.signals import update_quantity_on_sale_cancellation
            from sales.signals import sale_cancelled_signal
            sale_cancelled_signal.send(update_quantity_on_sale_cancellation, instance=obj)
        return HttpResponse("Vente annulé avec succès.")
    return HttpResponseBadRequest("Bad request")


