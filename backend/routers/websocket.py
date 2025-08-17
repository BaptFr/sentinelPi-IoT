from fastapi import APIRouter, WebSocket
from backend.websocket.manager import manager


router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/raspberry/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await manager.connect(websocket, device_id)
    try:
        while True:
            # Raspberyy messages reception
            data = await websocket.receive_text()
            print(f"Message from Raspberry {device_id}: {data}")
            
    except:
        manager.disconnect(device_id)

