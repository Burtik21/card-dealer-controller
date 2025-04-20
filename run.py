import threading
import RPi.GPIO as GPIO
import time
from flask import Flask
from app import create_app
from app.drivers.pins import Pins
from app.drivers.calibration import Calibration

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
Pins.setup_pins()  # ale už NEBUDE obsahovat volání kalibrace

for button in BUTTONS:
    if button.pin is not None:
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ⬇️ Provést kalibraci PŘED Flaskem
print("🧭 Spouštím kalibraci...")
calibration = Calibration()
calibration.calibration_rotate()
print("✅ Kalibrace dokončena")

# Funkce pro Flask server
def start_flask():
    print("🚀 Flask API startuje...")
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

# Spuštění Flask serveru ve vlákně
flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

# Tvoje funkční tlačítka – beze změny
print("▶️ TEST režim: tlačítka + Flask paralelně")
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
