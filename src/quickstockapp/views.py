import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.db.models.functions import ExtractMonth, ExtractYear

from inventories.models import Inventory
from stores.models import Store
from products.models import Product
from sales.models import Sale


@login_required(login_url='/accounts/login/')
def home(request):
    if request.session.get("current_store_pk") is None:
        return redirect("stores:store_list")
    
    

    periods = Sale.objects.annotate(
        month=ExtractMonth('sale_date'), year=ExtractYear('sale_date')).values('month', 'year').distinct()
    periods = periods.filter(year=str(datetime.datetime.now().year)).order_by("-month")
    
    selected_month, selected_year = None, None

    # get period in get request
    current_period = request.GET.get("current_period", None)
    if current_period:
        # update session period
        request.session["current_period"] = current_period

    else:
        current_period = request.session.get("current_period", None)
        if not current_period:
            # get default period
            period_obj = periods.first()
            if period_obj:
                current_period = f"{period_obj['month']}-{period_obj['year']}"
                request.session["current_period"] = current_period
    
    # getting current month and year
    if current_period:
        selected_month, selected_year = current_period.split("-")

    store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))

    context = {
        "page_title": "Tableau de bord",
        "total_earned": Inventory.total_earned(store=store, month=selected_month, year=selected_year),
        "net_incomme": Inventory.net_incomme(store=store, month=selected_month, year=selected_year),
        "shipping_fees": Inventory.get_shipping_fees(store=store, month=selected_month, year=selected_year),
        "sales_count": Inventory.sales_count(store=store, month=selected_month, year=selected_year),
        "products_count": Inventory.products_count(store=store),
        "best_products": Inventory.best_products(store=store, month=selected_month, year=selected_year),
        "out_of_stock_products": Inventory.out_of_stock_products(store=store),
        "total_stock": Inventory.get_total_stock(store=store),
        "periods": periods,
        "current_month": int(selected_month) if selected_month is not None else selected_month,
        "current_year": int(selected_year) if selected_year is not None else selected_year,
    }
    
    return render(request, "quickstockapp/dashboard.html", context=context)



