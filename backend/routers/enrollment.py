from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database.database import get_db
from backend.models.admins import Admin
from backend.models.lock_users import User
from backend.schemas.lock_user import UserCreate, EnrollmentConfirm
from backend.security.oauth2 import get_current_admin
from backend.services.lock_users_service import create_user_in_db
import uuid, requests

router = APIRouter(prefix="/enrollment", tags=["enrollment"])


#Temporary memory storage for enrolments(waiting for fingerprints confirmaiton)
temporary_enrollments: Dict[str, Any] = {}

def generate_temporate_id():
    return str(uuid.uuid4())

def send_to_raspberry(enrollment_id):
    url = "http://respberry/start_enrollment"
    data = {'enrollmentId': enrollment_id}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Enrollment sent to the raspberry")
    else:
        print("Error during the sending to the raspberry ")


#Starting enrolment route
@router.post("/start")
def start_enrollment(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):  
    enrollment_id = generate_temporate_id()
    temporary_enrollments[enrollment_id] = {
        'lastname': user.lastname,
        'firstname': user.firstname,
        'role': user.role,
        'status': 'pending'
    }

    send_to_raspberry(enrollment_id)
    return{"enrollmentId": enrollment_id}


#Enrollment confirmation route
@router.post("/confirm")
def confirm_enrollment(
    enrollment_data: EnrollmentConfirm, 
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    if enrollment_data.enrollment_id in temporary_enrollments:
        user_info = temporary_enrollments.pop(enrollment_data.enrollment_id)
        user_info['fingerprint'] = enrollment_data.fingerprint_id
        return create_user_in_db(db, user_info, fingerprint_path=user_info['fingerprint'])
    else:
        raise HTTPException(status_code=400, detail="Invalid enrollment ")
    
