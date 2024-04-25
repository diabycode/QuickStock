from django.shortcuts import redirect


class NotCurrentStoreMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.session.get("current_store_pk") is None:
            return redirect("stores:store_list")
        return super().dispatch(request, *args, **kwargs)

