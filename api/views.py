from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Station, Charger, Transaction
from .serializers import StationSerializer, ChargerSerializer, TransactionSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Station Views
class StationList(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Charger Views
class ChargerList(generics.ListCreateAPIView):
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        station_id = self.request.data.get('station')
        station = get_object_or_404(Station, id=station_id, admin=self.request.user)
        serializer.save(station=station)

class ChargerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializer
    permission_classes = [permissions.IsAuthenticated]

# Transaction Views
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        charger_id = self.request.data.get('charger')
        charger = get_object_or_404(Charger, id=charger_id)
        serializer.save(user=self.request.user, charger=charger)

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# Custom API Views for Remote Charging
class StartCharging(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, charger_id):
        charger = get_object_or_404(Charger, id=charger_id)
        if charger.status != 'Available':
            return Response({"error": "Charger is not available"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new transaction
        transaction = Transaction.objects.create(
            charger=charger,
            user=request.user,
        )
        charger.status = 'Occupied'
        charger.save()

        return Response({"message": "Charging started", "transaction_id": transaction.id}, status=status.HTTP_201_CREATED)

class StopCharging(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, charger_id):
        charger = get_object_or_404(Charger, id=charger_id)
        transaction = Transaction.objects.filter(charger=charger, end_time__isnull=True).first()

        if not transaction:
            return Response({"error": "No active transaction found"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the transaction and charger status
        transaction.end_time = timezone.now()
        transaction.save()
        charger.status = 'Available'
        charger.save()

        return Response({"message": "Charging stopped", "transaction_id": transaction.id}, status=status.HTTP_200_OK)