 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database.database import get_db
from backend.models.admins import Admin
from backend.models.lock_users import User
from backend.schemas.lock_user import UserCreate, EnrollmentConfirm
from backend.security.oauth2 import get_current_admin
from backend.services.lock_users_service import create_user_in_db
from backend.core.config import settings
from backend.websocket.manager import manager
import uuid, requests, asyncio

router = APIRouter(prefix="/api/enrollment", tags=["enrollment"])

#Variable
RASPBERRY_URL = settings.RASPBERRY_URL

#Temporary memory storage for enrolments(waiting for fingerprints confirmaiton)
temporary_enrollments: Dict[str, Any] = {}

#Pour TEST POSTMAN simulation retour du Raspberry Route: /confirm 
# temporary_enrollments["test"] = {
#     'lastname': "Doe",
#     'firstname': "John",
#      'role': "user",
#     'status': 'pending'
#  }


def generate_temporate_id():
    return str(uuid.uuid4())

#LOCAL NETWORK VERSION
# def send_to_raspberry(enrollment_id):
#     url = RASPBERRY_URL + "/start_enrollment"
#     data = {'enrollment_id': enrollment_id}
#     try:
#         response = requests.post(url, json=data, timeout= 30)

#         if response.status_code == 200:
#             print("Enrollment sent to the raspberry")
#         else:
#             print("Error during the sending to the raspberry, statuscode: ", response.status_code)
#     except requests.exceptions.RequestException as e :
#         print("Error during the snding to the Raspberry:", e)
async def send_to_raspberry(enrollment_id):
    #Websocket
    success = await manager.send_enrollment_to_raspberry(enrollment_id)
    if success:
        print("Enrollment sent to raspberry at WebSocket")
    else:
        print("No Raspberry connected to WebSocket ")






#Starting enrolment route
@router.post("/start")
async def start_enrollment(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    #Temporry User creation with pending status
    enrollment_id = generate_temporate_id()
    temporary_enrollments[enrollment_id] = {
        'lastname': user.lastname,
        'firstname': user.firstname,
        'role': user.role,
        'status': 'pending'
    }

    await send_to_raspberry(enrollment_id)
    return{"enrollment_id": enrollment_id}

#Enrollment confirmation route
@router.post("/confirm")
def confirm_enrollment(
    enrollment_data: EnrollmentConfirm,
    db: Session = Depends(get_db),
    # current_admin: Admin = Depends(get_current_admin) ### Not internal resquest
):
    print("Available in temporty enrollments:", temporary_enrollments.keys())
    #Current confirm verification with temporary User created / and adding
    if enrollment_data.enrollment_id in temporary_enrollments:
        user_info = temporary_enrollments.pop(enrollment_data.enrollment_id)
        user_info['fingerprint'] = enrollment_data.fingerprint_id
        user_info['enrollment_id'] = enrollment_data.enrollment_id

        #Confirmed new User creation after confirmation
        return create_user_in_db(db, user_info, fingerprint_id=user_info['fingerprint'], enrollment_id=user_info['enrollment_id'])
    else:
         raise HTTPException(status_code=400, detail="Invalid enrollment ")

#Check status enrollment process
@router.get("/status")
def enrollment_status(enrollment_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.enrollment_id == enrollment_id).first()
    if user:
        return {"status": "completed"}
    else:
        return {"status": "pending"}
    