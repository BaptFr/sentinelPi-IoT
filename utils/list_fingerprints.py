from pyfingerprint.pyfingerprint import PyFingerprint

# Sensor Initialization
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

# Check each position for stored fingerprints
print("Listing fingerprints:")
for position in range(sensor.getStorageCapacity()):
    try:
        if sensor.loadTemplate(position):
            print(f"Fingerprint found at position #{position}")
    except Exception as e:
        pass 