import RPi.GPIO as GPIO
import time

SENSOR_PIN = 26  # GPIO pin pro Hallův senzor

# Nastavení GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)  # Nastavení pinu jako vstupního

try:
    print("Čekám na magnet...")

    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # Aktivní LOW (většina Hall senzorů)
            print("Magnet detekován!")
            time.sleep(0.5)  # Krátká pauza, aby to nepsalo tisíckrát za sekundu

except KeyboardInterrupt:
    print("\nUkončuji program...")
    GPIO.cleanup()
