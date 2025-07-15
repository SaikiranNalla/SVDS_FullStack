from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

# Define a list fo url Patterns

urlpatterns = [
    # To render Welcome msg
    path('', views.home, name ='home'),

    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('/admin', views.dashboard, name='admin'),
    # path('admin/dashboard/', views.dashboard, name='dashboard'),
    # path('admin/add/', views.add_order, name='add_order'),
    # path('admin/complete/<int:pk>/', views.complete_order, name='complete_order'),
    # path('admin/download/<int:pk>/', views.download_invoice, name='download_invoice'),
    ]