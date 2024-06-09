from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<str:pk>/details/', views.UserDetailsView.as_view(), name='user_details'),
    path('users/<str:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<str:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/<str:pk>/change_password/', views.change_user_password, name='change_user_password'),
    
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<str:pk>/update/', views.GroupUpdateView.as_view(), name='group_update'),
    path('groups/<str:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('details/', views.AccountDetailsView.as_view(), name='details'),
    path('update/', views.AccountUpdateView.as_view(), name='update'),
    path('password_changed/', views.password_changed, name='password_changed'),

    path('action_logs/', views.UserActionLogList.as_view(), name='action_logs'),
]

