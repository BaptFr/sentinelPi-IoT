from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.pending_messages: Dict[str, List[Dict[str, Any]]] = {}
    
    #Connection
    async def connect(self, websocket: WebSocket, device_id: str):
        await websocket.accept()
        self.active_connections[device_id] = websocket
        logger.info(f"Device {device_id} connected via WebSocket")
        print(f"{device_id} connected")
        
        #If messages in queue = send them 
        if device_id in self.pending_messages:
            for message in self.pending_messages[device_id]:
                try:
                    await websocket.send_text(json.dumps(message))
                    logger.info(f"Sent pending message to {device_id}")
                except Exception as e:
                    logger.error(f"Error sending pending message: {e}")
            del self.pending_messages[device_id]
    
    #Disconnect
    def disconnect(self, device_id: str):
        if device_id in self.active_connections:
            del self.active_connections[device_id]
            logger.info(f"Device {device_id} disconnected")
            print(f"{device_id} déconnecté")
    
    async def send_message(self, device_id: str, message: str):
        websocket = self.active_connections.get(device_id)
        if websocket:
            try:
                await websocket.send_text(message)
                return True
            except Exception as e:
                logger.error(f"Error sending message to {device_id}: {e}")
                self.disconnect(device_id)
                return False
        return False
    
    async def send_message_to_device(self, device_id: str, message: Dict[str, Any]) -> bool:
        if device_id in self.active_connections:
            try:
                websocket = self.active_connections[device_id]
                await websocket.send_text(json.dumps(message))
                logger.info(f"Message sent to device {device_id}: {message.get('type', 'unknown')}")
                return True
            except Exception as e:
                logger.error(f"Error sending message to {device_id}: {e}")

                self.disconnect(device_id)
                #Put message in queue
                self._queue_message(device_id, message)
                return False
        else:
            #Device disconnected - put in queue
            self._queue_message(device_id, message)
            logger.warning(f"Device {device_id} not connected, message queued")
            return False
    
    #Waiting queue
    def _queue_message(self, device_id: str, message: Dict[str, Any]):
        if device_id not in self.pending_messages:
            self.pending_messages[device_id] = []
        
        message["queued_at"] = datetime.now().isoformat()
        self.pending_messages[device_id].append(message)
        
        if len(self.pending_messages[device_id]) > 10:
            self.pending_messages[device_id].pop(0)
    

    #ENROLLMENT
    async def send_enrollment_to_raspberry(self, payload: Dict[str, Any]) -> bool:
        device_id = payload.get("device_id")
        if not device_id:
            logger.error("No device_id provided in enrollment payload")
            return False
            
        websocket = self.active_connections.get(device_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(payload))  #  send_text with JSON
                print(f"Enrollment sent to Raspberry {device_id}")
                return True
            except Exception as e:
                print(f"Error during sending to rasp{device_id}: {e}")
                self.disconnect(device_id)
                return False
        else:
            print(f"No Raspberry with this ID: {device_id}")
            return False
    
    def get_connected_devices(self) -> List[str]:
        return list(self.active_connections.keys())
    
    def is_device_connected(self, device_id: str) -> bool:
        return device_id in self.active_connections

manager = ConnectionManager()
