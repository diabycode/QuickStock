
from django.urls import path, include

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/details/', views.ProductDetailsView.as_view(), name='product_details'),
    path('<slug:slug>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
]
