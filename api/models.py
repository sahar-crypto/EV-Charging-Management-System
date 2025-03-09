from django.db import models
from frontend.models import CustomUser
from django.conf import settings

# Create your models here.

class Station(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    location = models.CharField(max_length=255, unique=True, null=False)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_stations', default=1)

    def __str__(self):
        return self.name

class Charger(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    charger_id = models.CharField(max_length=50, unique=True, null=False)
    model = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")
    activity = models.CharField(max_length=50, default="Idle")


    def __str__(self):
        return self.charger_id
    
class Transaction(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_transactions', default=1)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    energy_consumed = models.FloatField(default=0.0)

    def __str__(self):
        return f"Transaction {self.id} at {self.charger.charger_id}"
    

class StatusLog(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.charger.charger_id} - {self.status} at {self.timestamp}" 