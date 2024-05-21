
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('dashbord/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('sales/', include('sales.urls')),
    path('stores/', include('stores.urls')),
    path('settings/', include('settings.urls')),
    path('debts/', include('debts.urls')),
    path('', include('pwa.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = views.handler404
handler500 = views.handler500