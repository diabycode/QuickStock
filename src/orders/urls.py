from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<str:pk>/details/', views.OrderDetailsView.as_view(), name='order_details'),
    path('<str:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<str:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('<str:pk>/cancel/', views.cancel_order, name='order_cancel'),

]


