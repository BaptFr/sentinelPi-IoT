
from pyfingerprint.pyfingerprint import PyFingerprint, FINGERPRINT_CHARBUFFER1, FINGERPRINT_CHARBUFFER2
from dotenv import load_dotenv
import sys, os, time

from services.shared_state import verification_controller

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("BACKEND_IP =", os.getenv("BACKEND_IP"))


BACKEND_IP = os.getenv("BACKEND_IP")

##### x2 fingerprints for quality of the process

verification_controller.request_enrollment()
time.sleep(0.1)

#Sensor initialisation
try:
    # sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000) #PIN RASPBERRY
    sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000) #USB adaptator

    if not sensor.verifyPassword():
        raise ValueError('The fingerprint sensor is protected by password!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: {}'.format(e))
    verification_controller.enrollment_completed()
    exit(1)

# Saved fingerprionts infos
print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))



#Enrollment process
try:
    print("Put your finger on the sensor...")
    start_time = time.time()
    timeout = 12  #20sec limit max delay for process

    while not sensor.readImage():
        if time.time() - start_time > timeout:
            verification_controller.enrollment_completed()
            print("Waiting time limit. No fingerprint detected.",)
            exit(1)
        time.sleep(0.5)

    #Conversion and register
    sensor.convertImage(FINGERPRINT_CHARBUFFER1)

    #  fingerprint check
    result = sensor.searchTemplate()
    template_position = result[0]

    if template_position >= 0:
        verification_controller.enrollment_completed()
        print('This finger already exists at position #{}'.format(template_position))

        exit(0)

    print('Remove the finger from the sensor...')
    time.sleep(2)

    #Second fingerprint read
    print('Waiting for same finger on the sensor...')
    
    while not sensor.readImage():
        if time.time() - start_time > timeout:
            verification_controller.enrollment_completed()
            print("Waiting time limit exceeded for second fingerprint.")
            exit(1)
    

    sensor.convertImage(FINGERPRINT_CHARBUFFER2)

    #The x2 fingerprints comparison
    if sensor.compareCharacteristics() == 0:
        raise Exception('Fingerprints do not match')
        
    #Template cration and fingerprint saved
    sensor.createTemplate()
    positionNumber = sensor.storeTemplate()
    print('Locks user fingerprint enrolled successfully!')
    print('New template position #{}'.format(positionNumber))
    
    #Delay because continuous verify.py will restart
    print('Remove the finger')
    time.sleep(6)
    verification_controller.enrollment_completed()
    print(f"[Enroll] Success: Fingerprint enrolled at position #{positionNumber}")
    

except Exception as e:
    verification_controller.enrollment_completed()
    print('Operation failed!')
    print('Exception message: {}'.format(e))
    exit(1)
