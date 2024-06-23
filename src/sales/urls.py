from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path('', views.SaleListView.as_view(), name='sale_list'),
    path('<str:pk>/details/', views.SaleDetailsView.as_view(), name='sale_details'),
    path('<str:pk>/delete/', views.SaleDeleteView.as_view(), name='sale_delete'),
    path('<str:pk>/update/', views.SaleUpdateView.as_view(), name='sale_update'),
    path('<str:pk>/cancel/', views.cancel_sale, name='sale_cancel'),
    path('create/', views.SaleCreateView.as_view(), name='sale_create'),
    path('<str:sale_pk>/update_sale_product_quantity/', views.update_sale_product_quantity, name='sale_product_update'),
]



