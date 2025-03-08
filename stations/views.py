from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import asyncio
from .models import Charger, Transaction
from .consumers import ChargePointConsumer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_chargers(request):
    """ List all active chargers """
    chargers = Charger.objects.filter(is_connected=True)
    data = [{"id": charger.charger_id, "status": charger.status} for charger in chargers]
    return Response({"active_chargers": data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_charger_details(request, charger_id):
    """ Get details of a specific charger """
    charger = get_object_or_404(Charger, charger_id=charger_id)
    data = {
        "id": charger.charger_id,
        "status": charger.status,
        "last_heartbeat": charger.last_heartbeat,
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def start_charging(request, charger_id):
    """ Send a command to start charging """
    charger = get_object_or_404(Charger, charger_id=charger_id)
    
    if charger.is_connected:
        charge_point = ChargePoint(charger.charger_id, charger.websocket)
        await charge_point.remote_start_transaction(id_tag="12345", connector_id=1)
        return Response({"status": "Charging started remotely"})
    
    return Response({"error": "Charger not connected"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def stop_charging(request, charger_id):
    """ Send a command to stop charging """
    charger = get_object_or_404(Charger, charger_id=charger_id)
    
    if charger.is_connected:
        charge_point = ChargePoint(charger.charger_id, charger.websocket)
        await charge_point.remote_stop_transaction(transaction_id=12345)
        return Response({"status": "Charging stopped remotely"})
    
    return Response({"error": "Charger not connected"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_charger_config(request, charger_id):
    """ Update charger settings remotely """
    charger = get_object_or_404(Charger, charger_id=charger_id)
    
    # Get new config parameters from request
    config_data = request.data.get("config", {})
    if not config_data:
        return Response({"error": "No configuration provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Apply settings (this should be implemented in ChargePoint consumer)
    # Example: await charge_point.update_configuration(config_data)
    return Response({"status": "Configuration updated", "applied_config": config_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_logs(request, charger_id):
    """ Retrieve transaction logs for a specific charger """
    logs = TransactionLog.objects.filter(charger_id=charger_id)
    data = [{
        "transaction_id": log.transaction_id,
        "status": log.status,
        "start_time": log.start_time,
        "end_time": log.end_time,
        "energy_used": log.energy_used,
    } for log in logs]
    return Response({"transactions": data})
