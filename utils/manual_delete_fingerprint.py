from pyfingerprint.pyfingerprint import PyFingerprint


#Script to manually delete a fingerprint
def delete_fingerprint(sensor, position):
    try:
        if sensor.deleteTemplate(position):
            print(f"Fingerprint at position #{position} successfully deleted.")
        else:
            print(f"Failed to delete fingerprint at position #{position}.")
    except Exception as e:
        print('Error during deletion:', str(e))

# Sensor initialization
try:
    # sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000) #PIN RASPBERRY
    sensor = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000) #USB    
    if not sensor.verifyPassword():
        raise ValueError('The fingerprint sensor is protected by a password!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Error message:', str(e))
    exit(1)

# List stored fingerprints
print(f"Currently stored fingerprints: {sensor.getTemplateCount()}/{sensor.getStorageCapacity()}")

##############Delete a fingerprint at a specific position
position_to_delete = 2  ############Desired position

delete_fingerprint(sensor, position_to_delete)