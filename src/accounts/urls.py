from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('details/', views.AccountDetailsView.as_view(), name='details'),
    path('update/', views.AccountUpdateView.as_view(), name='update'),
    path('password_changed/', views.password_changed, name='password_changed'),

]

