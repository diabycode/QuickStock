from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from inventories.models import Inventory
from stores.models import Store


@login_required(login_url='/accounts/login/')
def home(request):
    if request.session.get("current_store_pk") is None:
        return redirect("stores:store_list")

    store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))

    context = {
        "page_title": "Tableau de bord",
        "total_earned": Inventory.total_earned(store=store),
        "sales_count": Inventory.sales_count(store=store),
        "products_count": Inventory.products_count(store=store),
        "best_products": Inventory.best_products(store=store),
        "out_of_stock_products": Inventory.out_of_stock_products(store=store),
    }
    
    return render(request, "quickstockapp/dashboard.html", context=context)



