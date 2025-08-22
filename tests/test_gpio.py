import RPi.GPIO as GPIO
import time

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
relay_pin = 17  # Change ce numéro si nécessaire
GPIO.setup(relay_pin, GPIO.OUT)

try:
    # Activer le relais
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Relais activé")
    time.sleep(5)

    # Désactiver le relais
    GPIO.output(relay_pin, GPIO.LOW)
    print("Relais désactivé")
    
finally:
    # Nettoyage
    GPIO.cleanup()
