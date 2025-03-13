from django.urls import path
from django.contrib.auth.views import LogoutView 
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_login, name='logout'),
    path('home/', views.home, name='home'),
    path('add_station/', views.add_station, name='add_station'),
    path('update_station/<int:station_id>/', views.update_station, name='update_station'),
    path('add_charger/<int:station_id>/', views.add_charger, name='add_charger'),
    path('update_charger/<int:charger_id>/', views.update_charger, name='update_charger'), 
    path('view_transactions/<int:station_id>/', views.view_transactions, name='view_transactions'),
    path('view_chargers/', views.view_chargers, name='view_chargers'),  
    path('charge_point/<int:charger_id>/', views.view_charger, name='view_charger'),  
    path('start_charging/<int:charger_id>/', views.start_charging, name='start_charging'),
    path('stop_charging/<int:charger_id>/', views.stop_charging, name='stop_charging'),
]
