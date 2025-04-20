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

# Nastavení GPIO
GPIO.setmode(GPIO.BCM)
for button in BUTTONS:
    if button.pin is not None:
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("▶️ TEST: bez Flasku, jen tlačítka")

try:
    while True:
        for button in BUTTONS:
            if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                time.sleep(0.3)
except KeyboardInterrupt:
    print("⛔ Ukončuji program")
finally:
    GPIO.cleanup()
