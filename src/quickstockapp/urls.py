
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('sales/', include('sales.urls')),
    path('stores/', include('stores.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

