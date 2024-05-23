import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Model
from django.http import HttpRequest
from django.views.defaults import ERROR_404_TEMPLATE_NAME

from inventories.models import Inventory
from stores.models import Store
from products.models import Product
from sales.models import Sale
from settings.models import EditableSettings


def get_current_period(request: HttpRequest, period_list) -> tuple:
    # get period in get request
    current_period = request.GET.get("current_period", None)

    if current_period:
        # update session period
        request.session["current_period"] = current_period
    else:
        current_period = request.session.get("current_period", None)

        if not current_period:
            # get default period
            period_obj = period_list.first()
            if period_obj:
                current_period = f"{period_obj['month']}-{period_obj['year']}"
                request.session["current_period"] = current_period

    return (request, current_period)

def get_period_list(model, date_field: str):
    periods = model.objects.annotate(
        month=ExtractMonth(date_field), year=ExtractYear(date_field)).values('month', 'year').distinct()
    periods = periods.order_by("-year", "-month")
    return periods

@login_required(login_url='/accounts/login/')
def home(request: HttpRequest):
    if request.session.get("current_store_pk") is None:
        return redirect("stores:store_list")

    show_stats = request.session.get("show_stats", None)
    pin_error = False
    if request.method == "POST":
        request_show_stats = request.POST.get("request_show_stats")
        if request_show_stats is "1":
            selected_pin_code = request.POST.get("pin_code")
            settings = EditableSettings.load()
            if selected_pin_code == settings.pin_code:
                show_stats = "1"
                request.session["show_stats"] = show_stats
            else:
                pin_error = True
        else:
            show_stats = None
            try:
                del request.session["show_stats"]
            except KeyError:
                pass

    now_period = {
        "month": datetime.datetime.now().month, 
        "year": datetime.datetime.now().year}

    periods = get_period_list(model=Sale, date_field="sale_date")

    selected_month, selected_year = None, None
    request, current_period = get_current_period(request=request, period_list=periods)
    
    # getting current month and year
    if current_period:
        selected_month, selected_year = current_period.split("-")

    store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))

    context = {
        "page_title": "Tableau de bord",
        "total_earned": None if not show_stats else Inventory.total_earned(store=store, month=selected_month, year=selected_year),
        "net_incomme": None if not show_stats else Inventory.net_incomme(store=store, month=selected_month, year=selected_year),
        "shipping_fees": None if not show_stats else Inventory.get_shipping_fees(store=store, month=selected_month, year=selected_year, string=True),
        "sales_count": Inventory.sales_count(store=store, month=selected_month, year=selected_year),
        "products_count": Inventory.products_count(store=store),
        "best_products": Inventory.best_products(store=store, month=selected_month, year=selected_year),
        "out_of_stock_products": Inventory.out_of_stock_products(store=store),
        "total_stock": Inventory.get_total_stock(store=store),
        "periods": periods,
        "now_period": now_period,
        "current_month": int(selected_month) if selected_month is not None else selected_month,
        "current_year": int(selected_year) if selected_year is not None else selected_year,
        "recent_sales": Inventory.get_recent_sales(store=store, month=selected_month, year=selected_year, limit=5),
        "pin_error": pin_error,
        "show_stats": show_stats,
    }
    
    return render(request, "quickstockapp/dashboard.html", context=context)

def handler404(request, exception=None):
    return render(request, "quickstockapp/404.html")

def handler500(request, exception=None):
    return render(request, "quickstockapp/500.html")


