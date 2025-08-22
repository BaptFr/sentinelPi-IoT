from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from services.delete import delete_fingerprint
from services.verify import verify_fingerprints
from services.shared_state import verification_controller
from services.ws_client import start_continuous_verification, listen 

import requests
import subprocess
import threading
import time
import asyncio
import os

app = FastAPI()
load_dotenv()

#Variables
BACKEND_IP = os.getenv("BACKEND_IP")

#states
enrollment_in_progress = False
sensor_availability = threading.Lock()

if __name__ == "__main__":
    print("[Main] Starting fingerprint system")
    start_continuous_verification()
    asyncio.run(listen())    