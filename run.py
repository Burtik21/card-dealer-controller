import threading
import RPi.GPIO as GPIO
import time
from flask import Flask
from app import create_app
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

# Spuštění Flask serveru v druhém vlákně
def run_flask():
    print("🚀 Spouštím Flask...")
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

# Poslech tlačítek – zůstává beze změny
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

# Hlavní část
if __name__ == "__main__":
    # Spusť Flask jako druhé vlákno
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Spusť TLAČÍTKA v hlavním vlákně (nech to tak jak máš!)
    listen_to_buttons()
