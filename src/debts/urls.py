from django.urls import path

from . import views

app_name = "debts"

urlpatterns = [
    path('', views.DebtListView.as_view(), name='debt_list'),
    path('create/', views.DebtCreateView.as_view(), name='debt_create'),
    path('<str:pk>/details/', views.DebtDetailView.as_view(), name='debt_details'),
    path('<str:pk>/update/', views.DebtUpdateView.as_view(), name='debt_update'),
    path('<str:debt_pk>/repayment/', views.debt_repayment, name='debt_repayment'),
    path('<str:debt_pk>/repayments/<str:repayment_pk>/delete/', views.repayment_delete, name='repayment_delete'),
    path('<str:debt_pk>/repayments/<str:repayment_pk>/edit', views.edit_repayment, name='edit_repayment'),
    path('<str:pk>/delete/', views.DebtDeleteView.as_view(), name='debt_delete'),
]



