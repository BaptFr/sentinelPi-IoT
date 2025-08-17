from fastapi import APIRouter, WebSocket
from backend.websocket.manager import manager
import json
import logging

router = APIRouter(prefix="/ws/raspberry", tags=["websocket"])

@router.websocket("/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    print(f"WS connection requested for {device_id}")
    
    try:
        await manager.connect(websocket, device_id)
        
        await websocket.send_text(json.dumps({
            "type": "connection_confirmed",
            "device_id": device_id,
            "message": "Successfully connected to backend"
        }))
        
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Message from Raspberry {device_id}: {data}")
                
                try:
                    message = json.loads(data)
                    await handle_device_message(device_id, message, websocket)
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {device_id}: {data}")
                    
            except WebSocketDisconnect:
                print(f"Device {device_id} disconnected normally")
                break
                
    except Exception as e:
        print(f"WebSocket error for {device_id}: {e}")
    finally:
        manager.disconnect(device_id)

async def handle_device_message(device_id: str, message: dict, websocket: WebSocket):
    message_type = message.get("type")
    
    if message_type == "enrollment_result":
        print(f"Enrollment result from {device_id}: {message}")
        
    elif message_type == "heartbeat":
        await websocket.send_text(json.dumps({
            "type": "heartbeat_ack",
            "timestamp": message.get("timestamp")
        }))
    

@router.get("/status")
async def websocket_status():
    """Endpoint pour vérifier le statut des connexions WebSocket"""
    connected_devices = manager.get_connected_devices()
    return {
        "connected_devices": connected_devices,
        "total_connections": len(connected_devices)
    }


