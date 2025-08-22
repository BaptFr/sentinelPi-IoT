import time
import asyncio
import websockets
import json
import requests
import os

from pyfingerprint.pyfingerprint import PyFingerprint, FINGERPRINT_CHARBUFFER1
from services.lock_control import unlock_door
from services.shared_state import verification_controller

from dotenv import load_dotenv



#LOGS
async def send_backend_log_ws(status: str, websocket=None, template_position=None, score=None):
    if not hasattr(websocket, 'send'):
        return
    log_message = {
        "action": "access_log",
        "status": status
    }
    if template_position is not None:
        log_message["position"] = template_position
    if score is not None:
        log_message["score"] = str(score)

    try:
        await websocket.send(json.dumps(log_message))
        print(f"[Logs][WS] Sent: {log_message}")
    except Exception as e:
        print(f"[Logs][WS] Failed to send: {e}")

         
async def on_match_success(template_position, accuracy_score, websocket):
    print(f"Access granted: Position {template_position}, Score {accuracy_score}")
    
    print(f"Lock opening try:")
    try:
        unlock_door()
        log_status = "Accès accordé et ouverture de la serrure"
        print(f"Lock opening try : SUCCESS")
    except Exception as e:
        log_status = "Accès accordé mais problème d'ouverture de la serrure"
        print(f"Failed to unlock door: {e}")
        
    await send_backend_log_ws(log_status, websocket, template_position, accuracy_score)

         
#Verify failed function
async def on_match_failed(template_position, accuracy_score, websocket):
    print("Access denied")
    await send_backend_log_ws("Refusé", websocket=websocket, score=str(accuracy_score))

   
#Fingerprint sensor continuing function
def verify_fingerprints(websocket):
    try:
        print("Initializing sensor")
        # sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000) #PIN RASPBERRY
        sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000) #USB
        print("Verifying sensor password")
        if not sensor.verifyPassword():
            raise ValueError('The fingerprint sensor is protected by a password!')
        
        template_count = sensor.getTemplateCount()
        storage_capacity = sensor.getStorageCapacity()
        print(f'Stored fingerprints: {template_count}/{storage_capacity}')

        while verification_controller.is_verification_active():
            print('Waiting for finger...')
        
            while not sensor.readImage():
                if not verification_controller.is_verification_active():
                    print("continuous verification stopped: Enrollement or Deleting action")
                    return
                time.sleep(0.1)
            
            sensor.convertImage(FINGERPRINT_CHARBUFFER1)
            result = sensor.searchTemplate()
            template_position = result[0]
            accuracy_score = result[1]
              
            if template_position == -1:
                accuracy_score = 0
                asyncio.run(on_match_failed(template_position, accuracy_score, websocket=websocket))
            else:
                asyncio.run(on_match_success(template_position, accuracy_score, websocket=websocket))
            
            # cooldown  
            for _ in range(20): 
                if not verification_controller.is_verification_active():
                    return
                time.sleep(0.1)

    except Exception as e:
        print('Verification process failed ')
        print(f'Exception message: {e}')


#Start verif
def start_verification():
    print("Starting verification process")
    verification_controller.request_enrollment()
    
  #Stop verif
def stop_verification_process():
    print("Starting verification process for enrollment")
    verification_controller.enrollment_completed()
    