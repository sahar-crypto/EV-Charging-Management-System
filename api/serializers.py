from rest_framework import serializers
from .models import Station, Charger, Transaction

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['name', 'location', 'admin']

class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = ['station', 'charger_id', 'status', 'model', 'vendor', 'activity']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['charger', 'user', 'start_time', 'end_time', 'energy_consumed']