import datetime

from django.http import HttpRequest


def now_date(request: HttpRequest):
    return {"now_date": datetime.datetime.now().date().strftime("%Y-%m-%d")}

def current_tab(request: HttpRequest):
    context = {"current_tab": "current_tab"}
    
    if "/dashbord/" in request.path:
        context["current_tab"] = "dashbord"
    if "/products/" in request.path:
        context["current_tab"] = "products"
    if "/orders/" in request.path:
        context["current_tab"] = "orders"
    if "/sales/" in request.path:
        context["current_tab"] = "sales"

    return context
