from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, StationForm, ChargerForm
from api.models import Station, Charger, Transaction
import requests
from django.conf import settings

# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:  # Check if the user is an admin
            stations = Station.objects.filter(admin=request.user)
            return render(request, 'admin_home.html', {
                'stations': stations,
                'no_stations': not stations.exists(),  # Flag to indicate no stations
            })
        else:
            stations = Station.objects.all()
            return render(request, 'user_home.html', {
                'stations': stations,
            })
    else:
        return redirect('login')

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.admin = request.user
            station.save()
            return redirect('home')
    else:
        form = StationForm()
    return render(request, 'add_station.html', {'form': form})

def update_station(request, station_id):
    station = Station.objects.get(id=station_id)
    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StationForm(instance=station)
    return render(request, 'update_station.html', {'form': form})

def view_transactions(request, station_id):
    station = Station.objects.get(id=station_id)
    transactions = Transaction.objects.filter(charger__station=station)
    return render(request, 'view_transactions.html', {
                'transactions': transactions,
                'no_transactions': not transactions.exists(),  
            })

# def manage_charger(request, charger_id):
#     charger = Charger.objects.get(id=charger_id)
#     if request.method == 'POST':
#         form = ChargerForm(request.POST, instance=charger)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ChargerForm(instance=charger)
#     return render(request, 'manage_charger.html', {'form': form})

def start_charging(request, charger_id):
    if request.method == 'POST':
        response = requests.post(
            f'{settings.API_BASE_URL}/start_charging/{charger_id}/',
            headers={'Authorization': f'Bearer {request.user.auth_token.key}'}
        )
        if response.status_code == 201:
            return redirect('home')
        else:
            return render(request, 'error.html', {'error': response.json().get('error')})
    return redirect('home')

def stop_charging(request, charger_id):
    if request.method == 'POST':
        response = requests.post(
            f'{settings.API_BASE_URL}/stop_charging/{charger_id}/',
            headers={'Authorization': f'Bearer {request.user.auth_token.key}'}
        )
        if response.status_code == 200:
            return redirect('home')
        else:
            return render(request, 'error.html', {'error': response.json().get('error')})
    return redirect('home')