from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


def permission_required(permission, raise_exception=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                if raise_exception:
                    raise PermissionDenied("Accès interdit")
                return redirect(reverse("permission_denied"))  
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

