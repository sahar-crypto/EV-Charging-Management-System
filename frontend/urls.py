from django.urls import path
from django.contrib.auth.views import LogoutView 
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.user_login, name='login'),      # Login page
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('add_station/', views.add_station, name='add_station'),
    path('update_station/<int:station_id>/', views.update_station, name='update_station'),
    path('view_transactions/<int:station_id>/', views.view_transactions, name='view_transactions'),
]
#    path('manage_charger/<int:charger_id>/', views.manage_charger, name='manage_charger'),