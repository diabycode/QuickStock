from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from stores.models import Store

class NotCurrentStoreMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.session.get("current_store_pk") is None:
            store = Store.objects.first()
            if store:
                request.session["current_store_pk"] = store.pk
            else:
                request.session["current_store_pk"] = None
                return redirect("stores:store_create")
        else:
            try:
                get_object_or_404(Store, pk=request.session.get("current_store_pk"))
            except:
                store = Store.objects.first()
                if store:
                    request.session["current_store_pk"] = store.pk
                else:
                    request.session["current_store_pk"] = None
                    return redirect("stores:store_create")
        return super().dispatch(request, *args, **kwargs)

