import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on, create_route_map


logger = logging.getLogger(__name__)

class ChargePointConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ocpp_router = create_route_map(self)

    async def route_message(self, message):
        """ Route incoming OCPP messages to the appropriate handler """
        try:
            # Assuming message is a list where the first element is the message type
            message_type = message[0]
            payload = message[1]

            # Use the OCPP router to handle the message
            response = await self.ocpp_router.route_message(message_type, payload)
            if response:
                await self.send(text_data=json.dumps(response))
        except Exception as e:
            logger.error(f"Error routing message: {e}")
    
    async def connect(self):
        try:
            self.charger_id = self.scope["url_route"]["kwargs"]["charger_id"]
            self.group_name = f'charge_point_{self.charger_id}'

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"New connection: Charger {self.charger_id} connected.")
            logger.debug(f"WebSocket handshake headers: {self.scope['headers']}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")
            await self.close()
            

    async def disconnect(self, close_code):
        """ Handle WebSocket disconnection """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"Charger {self.charger_id} disconnected.")

    '''async def receive(self, text_data):
        """ Handle incoming WebSocket messages (OCPP Requests) """
        message = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'ocpp_message',
                'message': message
            }
        )
        logger.info(f"Received message from {self.charger_id}: {message}")
        await self.route_message(message)'''
    
    async def receive(self, text_data):
        """ Handle incoming WebSocket messages (OCPP Requests) """
        try:
            message = json.loads(text_data)
            if isinstance(message, list) and len(message) >= 2:
                await self.route_message(message)
            else:
                logger.error(f"Invalid message format: {message}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")

    async def ocpp_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        logger.info(f"Sent message to {self.charger_id}: {message}")


    async def send_status_update(self, status):
        """ Send a status update to the frontend """
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'charger_id': self.charger_id,
            'status': status,
        }))

    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ Handle BootNotification (sent by charger on startup) """
        logger.info(f"BootNotification received from {self.charger_id} - Model: {charge_point_model}")
        await self.send_status_update("Booted")
        return call_result.BootNotificationPayload(
            current_time="2025-02-26T12:00:00Z",
            interval=10,
            status="Accepted"
        )

    @on("Heartbeat")
    async def on_heartbeat(self, **kwargs):
        """ Handle Heartbeat messages (sent periodically by the charger) """
        logger.info(f"Heartbeat received from {self.charger_id}")
        await self.send_status_update("Heartbeat")
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
        
        await self.send_status_update(f"Authorize: {status}")
        return call_result.AuthorizePayload(
            id_tag_info={"status": status}
        )

    @on("StartTransaction")
    async def on_start_transaction(self, id_tag, connector_id, meter_start, **kwargs):
        """ Handle StartTransaction (when a user starts charging) """
        logger.info(f"StartTransaction received: Connector {connector_id}, ID {id_tag}")
        await self.send_status_update("Charging Started")
        return call_result.StartTransactionPayload(
            transaction_id=12345,
            id_tag_info={"status": "Accepted"}
        )

    @on("StopTransaction")
    async def on_stop_transaction(self, transaction_id, **kwargs):
        """ Handle StopTransaction (when a user stops charging) """
        logger.info(f"StopTransaction received: Transaction ID {transaction_id}")
        await self.send_status_update("Charging Stopped")
        return call_result.StopTransactionPayload()

    async def remote_start_transaction(self, id_tag, connector_id):
        """ Sends a RemoteStartTransaction command to the charger. """
        request = call.RemoteStartTransactionPayload(id_tag=id_tag, connector_id=connector_id)
        response = await self.call(request)  # Send request and wait for response
        
        if response.status == "Accepted":
            logger.info(f"Remote start successful for ID {id_tag} on Connector {connector_id}")
            await self.send_status_update("Remote Start: Accepted")
        else:
            logger.warning(f"Remote start failed for ID {id_tag} on Connector {connector_id}")
            await self.send_status_update("Remote Start: Failed")

        return response.status

    async def remote_stop_transaction(self, transaction_id):
        """ Sends a RemoteStopTransaction command to the charger. """
        request = call.RemoteStopTransactionPayload(transaction_id=transaction_id)
        response = await self.call(request)

        if response.status == "Accepted":
            logger.info(f"Remote stop successful for Transaction {transaction_id}")
            await self.send_status_update("Remote Stop: Accepted")
        else:
            logger.warning(f"Remote stop failed for Transaction {transaction_id}")
            await self.send_status_update("Remote Stop: Failed")

        return response.status

    async def unlock_connector(self, connector_id):
        """ Sends an UnlockConnector command to the charger. """
        request = call.UnlockConnectorPayload(connector_id=connector_id)
        response = await self.call(request)

        if response.status == "Unlocked":
            logger.info(f"Connector {connector_id} unlocked successfully")
            await self.send_status_update("Connector Unlocked")
        else:
            logger.warning(f"Failed to unlock Connector {connector_id}")
            await self.send_status_update("Connector Unlock Failed")

        return response.status