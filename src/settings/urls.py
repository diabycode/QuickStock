from django.urls import path

from . import views

app_name = "settings"

urlpatterns = [
    path('', views.SettingsUpdate.as_view(), name='setting_update'),
    path('delete_compagny_logo/', views.delete_compagny_logo, name='delete_compagny_logo'),
]



