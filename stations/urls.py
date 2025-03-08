from django.urls import path
from .views import StationView, TransactionView

urlpatterns = [
    path('stations/', StationView.as_view()),
    path('transactions/', TransactionView.as_view())
]
