from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.websocket.manager import manager
import json
import logging
import asyncio

router = APIRouter(prefix="/ws/raspberry", tags=["websocket"])


@router.websocket("/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    print(f"WS connection requested for {device_id}")

    await manager.connect(websocket, device_id)
    try:
        await websocket.send_text(json.dumps({
            "type": "connection_confirmed",
            "device_id": device_id,
            "message": "Successfully connected to backend"
        }))

        missed_heartbeats = 0
        MAX_MISSED = 5 

        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=10)
                missed_heartbeats = 0
                print(f"Message from Raspberry {device_id}: {data}")
                
                try:
                    message = json.loads(data)
                    await manager.handle_device_message(device_id, message)
                    await handle_device_message(device_id, message, websocket)
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {device_id}: {data}")
           
            except asyncio.TimeoutError:
                missed_heartbeats += 1
                print(f"Timeout waiting for {device_id} (missed {missed_heartbeats}/{MAX_MISSED})")
                if missed_heartbeats >= MAX_MISSED:
                    print(f"Device {device_id} seems disconnected, closing connection.")
                    break 
                await asyncio.sleep(0.1)
            
            
            except WebSocketDisconnect:
                print(f"Device {device_id} disconnected normally")
                break
                
    except Exception as e:
        print(f"WebSocket error for {device_id}: {e}")
    finally:
        manager.disconnect(device_id)

async def handle_device_message(device_id: str, message: dict, websocket: WebSocket):
    message_type = message.get("type")
    if message_type == "heartbeat":
        await websocket.send_text(json.dumps({
            "type": "heartbeat_ack",
            "timestamp": message.get("timestamp")
        }))
    elif message_type == "enrollment_result":
        print(f"Enrollment result from {device_id}: {message}")
    
    

@router.get("/status")
async def websocket_status():
    connected_devices = manager.get_connected_devices()
    return {
        "connected_devices": connected_devices,
        "total_connections": len(connected_devices)
    }


async def monitor_connections():
    while True:
        print("Active devices:", manager.get_connected_devices())
        await asyncio.sleep(10)

