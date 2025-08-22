import RPi.GPIO as GPIO
import time

def unlock_door():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # Number of the GPIO pin to #CONTROL !
    print("Opening lock...")
    GPIO.output(17, GPIO.HIGH)
    time.sleep(4)  # Open lock time
    GPIO.output(17, GPIO.LOW)
    print("Stop opening lock.")

    GPIO.cleanup()  