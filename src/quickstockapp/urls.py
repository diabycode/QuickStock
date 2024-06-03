
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashbord/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('sales/', include('sales.urls')),
    path('stores/', include('stores.urls')),
    path('settings/', include('settings.urls')),
    path('debts/', include('debts.urls')),
    path('pin_test_view/', views.pin_test_view, name="pin_test_view"),
    path('unlock_pin/', views.unlock_pin, name="unlock_pin"),
    path('lock_pin/', views.lock_pin, name="lock_pin"),
    path("display_stats/", views.display_stats, name="display_stats"),
    path('offline-page/', views.offline, name='offline'),
    path('pwa/', include('pwa.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.handler404
handler500 = views.handler500