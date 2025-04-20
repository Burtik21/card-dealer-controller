import threading
import RPi.GPIO as GPIO
import time
from app.drivers.pins import Pins

# Seznam tlačítek
BUTTONS = [
    Pins.BUTTON_1,
    Pins.BUTTON_2,
    Pins.BUTTON_3,
    Pins.BUTTON_4,
    Pins.BUTTON_5,
    Pins.BUTTON_6,
]

# Nastavení pinů
GPIO.setmode(GPIO.BCM)
for button in BUTTONS:
    if button.pin is not None:
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def listen_to_buttons():
    try:
        print("▶️ Testovací mód spuštěn – zmáčkni tlačítko...")
        while True:
            for button in BUTTONS:
                if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                    print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                    time.sleep(0.3)  # Debounce
    except KeyboardInterrupt:
        print("⛔ Ukončuji poslech tlačítek.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    listen_to_buttons()
