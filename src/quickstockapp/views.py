import datetime
import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Model
from django.http import HttpRequest
from django.urls import reverse
from django.views.defaults import ERROR_404_TEMPLATE_NAME

from inventories.models import Inventory
from stores.models import Store
from products.models import Product
from sales.models import Sale
from settings.models import EditableSettings
from accounts.models import UserPreference
from accounts.decorators import permission_required


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
def index(request: HttpRequest):
    return redirect(reverse("home"))

@login_required(login_url='/accounts/login/')
@permission_required("accounts.can_access_global_stats")
def home(request: HttpRequest):
    if request.session.get("current_store_pk") is None:
        return redirect("stores:store_list")

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
        "total_earned": Inventory.total_earned(store=store, month=selected_month, year=selected_year),
        "net_incomme": Inventory.net_incomme(store=store, month=selected_month, year=selected_year),
        "shipping_fees": Inventory.get_shipping_fees(store=store, month=selected_month, year=selected_year, string=True),
        "sales_count": Inventory.sales_count(store=store, month=selected_month, year=selected_year),
        "best_seller_products": Inventory.best_seller_products(store=store, month=selected_month, year=selected_year),
        "out_of_stock_products": Inventory.out_of_stock_products(store=store),
        "recent_sales": Inventory.get_recent_sales(store=store, month=selected_month, year=selected_year, limit=5),
        "periods": periods,
        "now_period": now_period,
        "current_month": int(selected_month) if selected_month is not None else selected_month,
        "current_year": int(selected_year) if selected_year is not None else selected_year,
    }
    
    return render(request, "quickstockapp/dashboard.html", context=context)


def handler404(request, exception=None):
    return render(request, "quickstockapp/404.html")


def handler500(request, exception=None):
    return render(request, "quickstockapp/500.html")


@login_required(login_url="/accounts/login/")
def offline(request: HttpRequest):
    return render(request,  "quickstockapp/offline.html", {"url": reverse("home")})


@login_required(login_url="/accounts/login/")
def pin_test_view(request):
    context = {}
    return render(request, "quickstockapp/pin_test_view.html", context)


@login_required(login_url="/accounts/login/")
def display_stats(request: HttpRequest):
    if request.method == "GET":
        pin_verified = request.session.get("pin_verified", None)
        if pin_verified:
            displayed = request.session.get("stats_displayed", None)
            if displayed:
                del request.session["stats_displayed"]
                return JsonResponse({"success": True})
            request.session["stats_displayed"] = "1"
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    return HttpResponseBadRequest("Bad request")


@login_required(login_url="/accounts/login/")
def unlock_pin(request: HttpRequest):
    if request.method == "POST":
        user_preference = UserPreference.objects.get(user=request.user)
        pin_code = json.loads(request.body.decode('utf-8')).get("pin_code")
        if pin_code and pin_code == user_preference.pin_code:
            request.session["pin_verified"] = "1"
            return JsonResponse({"test": "OK"})
        return JsonResponse({"test": "ERROR"})
    return HttpResponseBadRequest("Bad Request")


@login_required(login_url="/accounts/login/")
def lock_pin(request: HttpRequest):
    if request.method == "POST":
        del request.session["pin_verified"]
        return JsonResponse({"success": True})
    return HttpResponseBadRequest("Bad Request")


@login_required(login_url="/accounts/login/")
def permission_denied(request: HttpRequest):
    return render(request, "quickstockapp/permission_denied.html", {})






