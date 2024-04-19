from django.shortcuts import get_object_or_404

from stores.models import Store


def stores(request):
    stores = Store.objects.all()
    store_list = []
    for store in stores:
        store_list.append(
            (store.pk, store.name)
        )
    return {
        "current_store": get_object_or_404(Store, pk=request.session.get("current_store_pk")),
        "store_list": store_list
    }







