from django.urls import path

from stores import views


app_name = "stores"

urlpatterns = [
    path("", views.StoreListView.as_view(), name="store_list"),
    path("create/", views.StoreCreateView.as_view(), name="store_create"),
    path("<str:pk>/update/", views.StoreUpdateView.as_view(), name="store_update"),
    path("<str:pk>/delete/", views.StoreDeleteView.as_view(), name="store_delete"),
    path("change_store/<str:pk>/", views.change_store, name="change_store"),
]




