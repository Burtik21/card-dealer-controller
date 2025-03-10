import RPi.GPIO as GPIO
import time

# Nastavení GPIO režimu
GPIO.setmode(GPIO.BCM)

# Definice pinů tlačítek
BUTTON1_PIN = 21
BUTTON2_PIN = 20

# Nastavení pinů jako vstupy s interním pull-up rezistorem
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Stiskni tlačítko... (CTRL+C pro ukončení)")

try:
    while True:
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:
            print("Tlačítko 1 zmáčknuto!")
            time.sleep(0.2)  # Debouncing delay

        if GPIO.input(BUTTON2_PIN) == GPIO.LOW:
            print("Tlačítko 2 zmáčknuto!")
            time.sleep(0.2)  # Debouncing delay

except KeyboardInterrupt:
    print("Ukončuji program...")

finally:
    GPIO.cleanup()  # Resetuje GPIO
