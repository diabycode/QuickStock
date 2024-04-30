from django.shortcuts import get_object_or_404, redirect

from stores.models import Store


def stores(request):
    if not request.user.is_authenticated:
        return {}
    
    context = {}
    if request.session.get("current_store_pk") is None:
        return context
    
    try:
        current_store = get_object_or_404(Store, pk=request.session.get("current_store_pk"))
    except:
        return context
    
    context["current_store"] = current_store
    return context







