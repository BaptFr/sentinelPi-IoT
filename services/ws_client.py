
import asyncio
import websockets
import json
import os
import subprocess
import requests
import threading
import time

from dotenv import load_dotenv

from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from services.verify import verify_fingerprints, start_verification, stop_verification_process
from services.delete import delete_fingerprint as delete_fingerprint_service
from services.shared_state import verification_controller

load_dotenv()

BACKEND_IP = os.getenv("BACKEND_IP")
BACKEND_WS_URL = os.getenv("BACKEND_WS_URL")  
DEVICE_ID = os.getenv("DEVICE_ID")

enrollment_in_progress = threading.Event()
delete_in_progress = threading.Event()


async def listen():
   #Websocket listening
    while True:
        try:
            #Connect to backend
            print(f"[WS] Connecting to wss://{BACKEND_IP}/ws/raspberry/{DEVICE_ID}")
            
            async with websockets.connect(f"wss://{BACKEND_WS_URL}/{DEVICE_ID}", ping_interval=None) as websocket:
                print("[WS] Connected!")
                start_continuous_verification(websocket)  
            
                async def send_heartbeat():
                    while True:
                        try:
                            await websocket.send(json.dumps({"type": "heartbeat"}))
                        except (ConnectionClosedOK, ConnectionClosedError):
                            break
                        await asyncio.sleep(30)
                        
                asyncio.create_task(send_heartbeat())
                
                async for message in websocket:
                    data = json.loads(message)
                    
                    #ENROLLMENT action received
                    if data.get('action') == "start_enrollment":                      
                        if not enrollment_in_progress.is_set():
                            enrollment_in_progress.set()
                            asyncio.create_task(handle_enrollment(data['enrollment_id'], websocket))
                        else:
                            print("[WS] Enrollment already in progress, skipping")
                    
                    elif data.get('action') == "delete_fingerprint":
                        if not delete_in_progress.is_set():
                            delete_in_progress.set()
                            asyncio.create_task(handle_delete(data['fingerprint_id'], websocket))
                        else:
                            print("[WS] Delete already in progress, skipping")
                             
        except (ConnectionClosedOK, ConnectionClosedError):
            print("[WS] Connection closed by server, reconnecting in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[WS] Connection error: {e}, retrying in 5s")
            await asyncio.sleep(5)



#Enrollment process handling
async def handle_enrollment(enrollment_id, websocket):
    try:
        print(f"[WS][Enroll] Starting enrollment process for ID: {enrollment_id}")
        
        #Stop verif
        verification_controller.request_enrollment()
        print("[WS][Enroll] Verification stopped, starting enrollment")
        await asyncio.sleep(0.5) 
        
        #Launch enrollment
        process = await asyncio.create_subprocess_exec(
            "python3", "-m", "services.enroll", enrollment_id,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        )

        stdout_bytes, stderr_bytes = await process.communicate()
        stdout = stdout_bytes.decode() if stdout_bytes else ""
        stderr = stderr_bytes.decode() if stderr_bytes else ""

        if stdout:
            print(stdout)
        if stderr:
            print("[WS][Enroll][stderr]", stderr)
        
        fingerprint_id = None
        for token in stdout.strip().split():
            if token.startswith("#"):
                number_str = ''.join(filter(str.isdigit, token[1:]))
                if number_str:
                    fingerprint_id = int(number_str)
                    break
        if fingerprint_id is None:
            print("[WS][Enroll] fingerprint_id not found")
            return

        print(f"[WS][Enroll] Fingerprint ID: {fingerprint_id}")

        # Confirmation to backend
        backend_url = f"https://{BACKEND_IP}/api/enrollment/confirm"
        try:
            response = requests.post(backend_url, json={
                "enrollment_id": str(enrollment_id),
                "fingerprint_id": str(fingerprint_id),
                "device_id": str(DEVICE_ID)
            }, timeout=15)

            if response.status_code == 200:
                print("[WS][Enroll] Confirmation successfully sent to backend")
            else:
                print(f"[WS][Enroll]  Confirmation successfully sent to backend")

        except Exception as e:
            print(f"[WS][Enroll] Error sending to backend: {e}")

    except Exception as e:
        print(f"[WS][Enroll] Unexpected error during enrollment: {e}")
    
    finally:
        enrollment_in_progress.clear()
        verification_controller.enrollment_completed()
        print("[WS][Enroll] Enrollment process ending")
        time.sleep(1)


#Delete process handling
async def handle_delete(fingerprint_id: int, websocket):
    try:
        print(f"[WS][Delete] Attempting to delete fingerprint ID: {fingerprint_id}")
        
        #Stop the continuing Verify
        verification_controller.request_enrollment()
        await asyncio.sleep(0.2)
        
        result = delete_fingerprint_service(fingerprint_id)
        print(f"[WS][Delete] {result['message']}")
        
        await websocket.send(json.dumps({
            "action": "delete_confirmation",
            "fingerprint_id": fingerprint_id,
            "success": True,
            "message": result['message']
        }))

        print(f"[WS][Delete] Confirmation sent to backend")
        
    except Exception as e:
        print(f"[WS][Delete] Failed to delete fingerprint: {e}")
        
        if hasattr(websocket, 'send'):
            await websocket.send(json.dumps({
                "action": "delete_confirmation",
                "fingerprint_id": fingerprint_id,
                "success": False,
                "message": str(e)
            }))
        else:
            print("[WS][Delete] websocket object invalid, cannot send error confirmation")

    finally:
        delete_in_progress.clear()
        verification_controller.enrollment_completed()

def start_continuous_verification(websocket):
    def run_verification():
        while True:
            try:
                if verification_controller.is_verification_active():
                    print("[Verification] Starting fingerprint verification")
                    verify_fingerprints(websocket)
                else:
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"[Verification] Error in verification process: {e}")
                time.sleep(0.5)  
    #Saar verif
    threading.Thread(target=run_verification, daemon=True).start()
    print("[Verification] Continuous verification started")

if __name__ == "__main__":
    print("[Main] Starting WebSocket client with continuous verification")
    asyncio.run(listen())
    