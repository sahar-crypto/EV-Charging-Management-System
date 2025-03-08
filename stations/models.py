from django.db import models

# Create your models here.

class Station(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    location = models.CharField(max_length=255, unique=True, null=False)
    chargers = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.name

class Charger(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    charger_id = models.CharField(max_length=50, unique=True, null=False)
    model = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Available")

    def __str__(self):
        return self.charger_id
    

class Transaction(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.id} - {self.charger.charger_id}"
    

class StatusLog(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.charger.charger_id} - {self.status} at {self.timestamp}" 
