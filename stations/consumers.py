import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on

logger = logging.getLogger(__name__)

class ChargePointConsumer(AsyncWebsocketConsumer, cp):
    
    async def connect(self):
        """ Handle new WebSocket connection from an EV charger """
        self.charger_id = self.scope["url_route"]["kwargs"]["charger_id"]
        await self.accept()
        logger.info(f"New connection: Charger {self.charger_id} connected.")

    async def disconnect(self, close_code):
        """ Handle WebSocket disconnection """
        logger.info(f"Charger {self.charger_id} disconnected.")

    async def receive(self, text_data):
        """ Handle incoming WebSocket messages (OCPP Requests) """
        message = json.loads(text_data)
        logger.info(f"Received message from {self.charger_id}: {message}")
        await self.route_message(message)

    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Handle BootNotification (sent by charger on startup) """
        logger.info(f"BootNotification received from {self.charger_id} - Model: {charge_point_model}")
        return call_result.BootNotificationPayload(
            current_time="2025-02-26T12:00:00Z",
            interval=10,
            status="Accepted"
        )

    @on("Heartbeat")
    async def on_heartbeat(self, **kwargs):
        """ Handle Heartbeat messages (sent periodically by the charger) """
        logger.info(f"Heartbeat received from {self.charger_id}")
        return call_result.HeartbeatPayload(
            current_time="2025-02-26T12:00:00Z"
        )

    @on("Authorize")
    async def on_authorize(self, id_tag, **kwargs):
        """ Handle RFID card authentication """
        logger.info(f"Authorize request received for ID {id_tag} from {self.charger_id}")
        
        # Simulate checking RFID ID in the database
        valid_ids = ["EV123456789", "RFID987654"]
        status = "Accepted" if id_tag in valid_ids else "Invalid"
        
        return call_result.AuthorizePayload(
            id_tag_info={"status": status}
        )

    @on("StartTransaction")
    async def on_start_transaction(self, id_tag, connector_id, meter_start, **kwargs):
        """ Handle StartTransaction (when a user starts charging) """
        logger.info(f"StartTransaction received: Connector {connector_id}, ID {id_tag}")
        return call_result.StartTransactionPayload(
            transaction_id=12345,
            id_tag_info={"status": "Accepted"}
        )

    @on("StopTransaction")
    async def on_stop_transaction(self, transaction_id, **kwargs):
        """ Handle StopTransaction (when a user stops charging) """
        logger.info(f"StopTransaction received: Transaction ID {transaction_id}")
        return call_result.StopTransactionPayload()


    async def remote_start_transaction(self, id_tag, connector_id):
        """ Sends a RemoteStartTransaction command to the charger. """
        request = call.RemoteStartTransactionPayload(id_tag=id_tag, connector_id=connector_id)
        response = await self.call(request)  # Send request and wait for response
        
        if response.status == "Accepted":
            logger.info(f"Remote start successful for ID {id_tag} on Connector {connector_id}")
        else:
            logger.warning(f"Remote start failed for ID {id_tag} on Connector {connector_id}")

        return response.status
    

    async def remote_stop_transaction(self, transaction_id):
        """ Sends a RemoteStopTransaction command to the charger. """
        request = call.RemoteStopTransactionPayload(transaction_id=transaction_id)
        response = await self.call(request)

        if response.status == "Accepted":
            logger.info(f"Remote stop successful for Transaction {transaction_id}")
        else:
            logger.warning(f"Remote stop failed for Transaction {transaction_id}")

        return response.status
    

    async def unlock_connector(self, connector_id):
        """ Sends an UnlockConnector command to the charger. """
        request = call.UnlockConnectorPayload(connector_id=connector_id)
        response = await self.call(request)

        if response.status == "Unlocked":
            logger.info(f"Connector {connector_id} unlocked successfully")
        else:
            logger.warning(f"Failed to unlock Connector {connector_id}")

        return response.status
    




