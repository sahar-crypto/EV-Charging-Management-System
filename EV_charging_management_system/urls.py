from django.contrib import admin
from django.urls import path, include
from frontend.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', user_login, name='login'),
    path('home/', include('frontend.urls')),
    path('login/', include('frontend.urls')),
    path('register/', include('frontend.urls')),
    path('add_station/', include('frontend.urls')),
    path('update_station/<int:station_id>/', include('frontend.urls')),
    path('view_transactions/<int:station_id>/', include('frontend.urls')),
    path('manage_charger/<int:charger_id>/', include('frontend.urls')),
]