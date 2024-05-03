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

    store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))
    month_list = Sale.objects.annotate(
        month=ExtractMonth('sale_date'), year=ExtractYear('sale_date')).values('month', 'year').distinct()
    month_list = month_list.filter(year=str(datetime.datetime.now().year)).order_by("-month")
    
    month, year = None, None
    period_selected = request.GET.get("period")
    if period_selected:
        month, year = period_selected.split("-")

    best_products = []
    for p in Inventory.best_products(store=store, month=month, year=year):
        best_products.append(
            {
                "product": p,
                "count": p.get_sales_count()
            }
        )

    context = {
        "page_title": "Tableau de bord",
        "total_earned": Inventory.total_earned(store=store, month=month, year=year),
        "sales_count": Inventory.sales_count(store=store, month=month, year=year),
        "products_count": Inventory.products_count(store=store),
        "best_products": best_products,
        "out_of_stock_products": Inventory.out_of_stock_products(store=store),
        "total_stock": Inventory.get_total_stock(store=store),
        "month_list": month_list,
    }
    
    return render(request, "quickstockapp/dashboard.html", context=context)



