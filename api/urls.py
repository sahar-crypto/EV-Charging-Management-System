from django.urls import path
from . import views

urlpatterns = [
    # Station endpoints
    path('stations/', views.StationList.as_view(), name='station-list'),
    path('stations/<int:pk>/', views.StationDetail.as_view(), name='station-detail'),

    # Charger endpoints
    path('chargers/', views.ChargerList.as_view(), name='charger-list'),
    path('chargers/<int:pk>/', views.ChargerDetail.as_view(), name='charger-detail'),

    # Transaction endpoints
    path('transactions/', views.TransactionList.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),

    # Custom endpoints for remote charging
    path('start_charging/<int:charger_id>/', views.StartCharging.as_view(), name='start-charging'),
    path('stop_charging/<int:charger_id>/', views.StopCharging.as_view(), name='stop-charging'),
]