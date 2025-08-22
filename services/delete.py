from pyfingerprint.pyfingerprint import PyFingerprint

def init_sensor():
    try:
        # sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000) #PIN RASPBERRY
        sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000) #USB
        
        if not sensor.verifyPassword():
            raise Exception("incorrect sensos password")
        return sensor
    except Exception as e:
        raise Exception(f"Error during sensor initialisation: {e}")


def delete_fingerprint(fingerprint_id: int):
    sensor = init_sensor()
    
    try:
        fingerprint_id = int(fingerprint_id)
    except ValueError:
        raise Exception(f"Invalid fingerprint ID: {fingerprint_id}")
    
    count = sensor.getTemplateCount()
    capacity = sensor.getStorageCapacity()

    if fingerprint_id >= capacity or fingerprint_id < 0:
        raise Exception(f" Invalid fingerprint ID position #{fingerprint_id}: Position must between #0 and {capacity - 1}")

    if sensor.deleteTemplate(fingerprint_id):
        return {"message": f"Fingerprint {fingerprint_id} deleted"}
    else:
        raise Exception(f"Failed to delete fingerprint # {fingerprint_id}")
