from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, StationForm, ChargerForm
from api.models import Station, Charger, Transaction
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests
from requests.exceptions import RequestException

# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
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
            stations = Station.objects.prefetch_related('chargers').filter(admin=request.user)
            chargers = [Charger.objects.filter(station=station) for station in stations]
            return render(request, 'admin_home.html', {
                'stations': stations,
                'no_stations': not stations.exists(),
                'chargers': chargers,
                'no_chargers': len(chargers) == 0,
            })
        else:
            stations = Station.objects.all()
            return render(request, 'user_home.html', {
                'stations': stations,
            })
    else:
        return redirect('login')

@login_required
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

@login_required
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

@login_required
def add_charger(request, station_id):
    station = Station.objects.get(id=station_id)  # Get the station
    if request.method == 'POST':
        form = ChargerForm(request.POST)
        if form.is_valid():
            charger = form.save(commit=False)
            charger.station = station  # Assign station to charger
            charger.admin = request.user
            charger.save()
            return redirect('home')
    else:
        form = ChargerForm()
    return render(request, 'add_charger.html', {'form': form, 'station': station})

@login_required
def update_charger(request, charger_id):
    charger = Charger.objects.get(id=charger_id)
    if request.method == 'POST':
        form = ChargerForm(request.POST, instance=charger)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ChargerForm(instance=charger)
    return render(request, 'update_charger.html', {'form': form})

def view_transactions(request, station_id):
    station = Station.objects.get(id=station_id)
    transactions = Transaction.objects.filter(charger__station=station)
    return render(request, 'view_transactions.html', {
                'transactions': transactions,
                'no_transactions': not transactions.exists(),  
            })

def view_chargers(request, charger_id):
    chargers = Charger.objects.all()
    return render(request, 'view_chargers.html', {
        'chargers': chargers,
    })

def view_charger(request, charger_id):
    charger = Charger.objects.get(id=charger_id)
    return render(request, 'view_charger.html', {
        'charger': charger,
    })

def start_charging(request, charger_id):
    if request.method == 'POST':
        try:
            response = requests.post(
                f'{settings.API_BASE_URL}/start_charging/{charger_id}/',
                headers={'Authorization': f'Bearer {request.user.auth_token.key}'}
            )
            if response.status_code == 201:
                return redirect('home')
            else:
                return render(request, 'error.html', {'error': response.json().get('error', 'Unknown error')})
        except RequestException as e:
            return render(request, 'error.html', {'error': f'API request failed: {str(e)}'})

    return redirect('home')

def stop_charging(request, charger_id):
    if request.method == 'POST':
        try:
            response = requests.post(
                f'{settings.API_BASE_URL}/stop_charging/{charger_id}/',
                headers={'Authorization': f'Bearer {request.user.auth_token.key}'}
            )
            if response.status_code == 200:
                return redirect('home')
            else:
                return render(request, 'error.html', {'error': response.json().get('error')})
        except RequestException as e:
            return render(request, 'error.html', {'error': f'API request failed: {str(e)}'})
        
    return redirect('home')