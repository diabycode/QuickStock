import datetime

from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.forms.utils import ErrorList
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.core.exceptions import PermissionDenied
from unidecode import unidecode

from .models import Sale, SaleStatus
from stores.models import Store
from stores.mixins import NotCurrentStoreMixin
from products.models import Product
from quickstockapp.views import get_period_list, get_current_period
from accounts.utils import log_user_action
from accounts.mixins import MyPermissionRequiredMixin
from accounts.decorators import permission_required


class SaleListView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, ListView):

    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"
    permission_required = "sales.can_view_sale"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        sale_column_names = [
            Sale.sale_date.field.verbose_name,
            Sale.status.field.verbose_name,
            Sale.store.field.verbose_name,
            Sale.seller.field.verbose_name,
            Sale.products.field.verbose_name,
        ]
        
        local_date_format = "%d/%m/%Y"
        today = datetime.datetime.now().date()

        
        # date range selected
        date_range: str | None = self.request.GET.get("dates", None)
        from_date, to_date = (today, today)
        is_today = True
        if date_range is not None:
            if not self.request.user.has_perm("accounts.can_access_global_stats"):
                raise PermissionDenied()
            from quickstockapp.views import get_date_objects_from_date_range
            from_date, to_date = get_date_objects_from_date_range(date_range)
            is_today = False

        store = get_object_or_404(Store, pk=self.request.session.get("current_store_pk"))
        sale_list = Sale.objects.filter(store=store, sale_date__range=[from_date, to_date])            
        
        date_range_max = Sale.objects.last().sale_date if Sale.objects.last() else None
        date_range_min = Sale.objects.first().sale_date if Sale.objects.first() else None

        # search query filters
        isfilters = False
        search_query = self.request.GET.get("q", None)
        if search_query:
            isfilters = True
            def func(s):
                product_names = [p.unaccent_name.lower() for p in s.products.all()]
                for name in product_names:
                    if unidecode(search_query).lower() in name:
                        return True
                return False
            sale_list = filter(func, sale_list)

        context["day_sale_number"] = Sale.get_day_sale_number(store=store)
        context["day_sale_revenue"] = Sale.get_day_sale_revenue(store=store)
        context["day_sale_product_quantity"] = Sale.get_day_sale_product_quantity(store=store)
        context["sale_column_names"] = sale_column_names
        context["sale_list"] = sale_list
        context["page_title"] = "Ventes"
        context["isfilters"] = isfilters

        context["from_date"] = from_date.strftime(local_date_format)
        context["to_date"] = to_date.strftime(local_date_format)
        context["date_range_max"] = date_range_max.strftime(local_date_format) if date_range_max else today.strftime(local_date_format)
        context["date_range_min"] = date_range_min.strftime(local_date_format) if date_range_min else today.strftime(local_date_format)
        context["is_today"] = is_today 
        
        if search_query:
            context["search_query"] = search_query 
        return context


class SaleDetailsView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DetailView):
    model = Sale
    template_name = "sales/sale_details.html"
    context_object_name = "sale"
    extra_context = {"page_title": "Ventes"}
    permission_required = "sales.can_view_sale"


class SaleCreateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, CreateView):

    model = Sale
    fields = [
        'sale_date',
        'products',
        'store',
        'buyer_name',
        'buyer_phone',
        'seller',
        'discount'
    ]
    template_name = "sales/sale_create.html"
    # success_url = reverse_lazy("sales:sale_list")
    extra_context = {"page_title": "Ventes"}
    permission_required = "sales.can_add_sale"

    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            form_data = form.cleaned_data

            # check date error
            sale_date: datetime.date = form_data.get("sale_date")
            now_date = datetime.datetime.now().date()
            if sale_date > now_date:
                form.add_error("sale_date", "Erreur de date")
                return self.form_invalid(form=form)
            
            # status error
            if form_data.get("status") == SaleStatus.CANCELLED:
                form.add_error("status", "Impossible d'ajouter une vente annulée")
                return self.form_invalid(form=form)
            
            # product quantity error
            products = form_data.get("products")
            for product in products:
                if product.stock_quantity <= 0:
                    form.add_error("products", "Vous essayez de vendre un produit à stock insufisant")
                    return self.form_invalid(form=form)

        form_valid_response = super().form_valid(form) 
        instance: Sale = form.instance
        if instance.discount:
            instance.discount_applied = True
            instance.save()

        log_user_action(
            user=self.request.user,
            obj=form.instance,
            action_flag=ADDITION,
            change_message="Vente ajouté"
        )
        return form_valid_response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        current_store = self.request.session.get("current_store_pk", None)
        from stores.models import Store
        if current_store:
            form.fields["store"].initial = get_object_or_404(Store, pk=current_store)

        store = get_object_or_404(Store, pk=current_store)
        form.fields["products"].queryset = Product.objects.filter(store=store)
        form.fields["products"].help_text = "Ajoutez des porduits et selectionnez leur quantité juste après."
        form.fields["seller"].initial = self.request.user
        form.fields["seller"].disabled = True
        form.fields["store"].disabled = True
        return form

    def get_success_url(self) -> str:
        instance = self.get_form().instance
        success_url = reverse("sales:sale_product_update", kwargs={"sale_pk": instance.pk})
        return success_url


class SaleUpdateView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, UpdateView):
    model = Sale
    fields = [
        'sale_date',
        'products',
        'store',
        'buyer_name',
        'buyer_phone',
        'seller',
        'discount'
    ]
    template_name = "sales/sale_update.html"
    extra_context = {"page_title": "Ventes"}
    permission_required = "sales.can_change_sale"
    context_object_name = "sale"
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["seller"].disabled = True
        form.fields["products"].disabled = True
        form.fields["store"].disabled = True
        return form
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:

        if form.is_valid():
            sale_date: datetime.date = form.cleaned_data.get("sale_date")
            now_date = datetime.datetime.now().date()

            if sale_date > now_date:
                form.add_error("sale_date", "Erreur de date")
                return self.form_invalid(form=form)

        # verif if locked fields got changes
        locked_fields = [
            (field_name, field) for (field_name, field) in form.fields.items() 
            if field.disabled == True
        ]
        for field_name, field in locked_fields:
            if field_name in form.changed_data:
                return HttpResponseBadRequest("Erreur: Le champ '{}' ne doit être changé.".format(field.label))

        obj: Sale = form.instance
        if obj.discount:
            obj.discount_applied = True
        obj.save()
        log_user_action(
            user=self.request.user,
            action_flag=CHANGE,
            obj=form.instance,
            change_message="Vente modifié"
        )
        return redirect(reverse("sales:sale_details", kwargs={"pk": obj.pk}))

    def get_success_url(self) -> str:
        return reverse("sales:sale_details", kwargs={"pk": self.kwargs.get("pk")})


class SaleDeleteView(LoginRequiredMixin, MyPermissionRequiredMixin, NotCurrentStoreMixin, DeleteView):
    model = Sale
    context_object_name = "sale"
    template_name = "sales/sale_delete.html"
    success_url = reverse_lazy("sales:sale_list")
    extra_context = {"page_title": "Ventes"}
    permission_required = "sales.can_delete_sale"

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != "2":
            return HttpResponseBadRequest("Bad request")
        
        log_user_action(
            user=self.request.user,
            action_flag=DELETION,
            obj=self.get_object(),
            change_message="Vente supprimé"
        )
        return super().post(request=request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
@permission_required("sales.can_change_sale")
def cancel_sale(request, pk):
    context = {}
    obj: Sale = get_object_or_404(Sale, pk=pk)

    if request.method == "POST":
        obj.status = SaleStatus.CANCELLED
        obj.save()

        if request.POST.get("restore_stock") == "on":
            from sales.signals import restore_stock
            restore_stock.send(sender=Sale, instance=obj)
        return redirect(reverse("sales:sale_details", kwargs={"pk": obj.pk}))
    context["sale"] = obj
    return render(request, "sales/sale_cancel.html", context)


def update_sale_product_quantity(request: HttpRequest, sale_pk):
    sale = get_object_or_404(Sale, pk=sale_pk)
    saleproducts = sale.saleproduct_set.all()

    if request.method == "POST":
        form_data = request.POST
        for saleproduct in saleproducts:
            if form_data.get(f"quantity-{saleproduct.pk}"):
                saleproduct.quantity = form_data.get(f"quantity-{saleproduct.pk}")
                saleproduct.save()

        # print(form_data)
        if form_data.get("deduct_from_stock") == "on":
            from sales.signals import deduct_sale_from_stock
            deduct_sale_from_stock.send(Sale, instance=sale)
        return redirect(reverse("sales:sale_details", kwargs={"pk": sale.pk}))

    context = {
        "saleproducts": saleproducts
    }
    return render(request, "sales/update_sale_product_quantity.html", context)