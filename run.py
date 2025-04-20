import threading
import RPi.GPIO as GPIO
import time
import requests
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

# GPIO setup
GPIO.setmode(GPIO.BCM)
Pins.setup_pins()

for button in BUTTONS:
    if button.pin is not None:
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Kalibrace před spuštěním
print("🧭 Spouštím kalibraci...")
calibration = Calibration()
calibration.calibration_rotate()
print("✅ Kalibrace dokončena")

# 📤 Posílání do Node.js backendu
def notify_node(button_index):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/deal",  # změň na IP/port podle backendu
            json={"button": button_index}
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_index} | Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání do Node.js: {e}")

# 👉 Poslech tlačítek ve vlákně
def listen_to_buttons():
    try:
        print("▶️ Poslouchám tlačítka...")
        while True:
            for button in BUTTONS:
                if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                    print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                    notify_node(button.index)
                    time.sleep(0.3)
    except KeyboardInterrupt:
        print("⛔ Ukončuji poslech tlačítek.")
    finally:
        GPIO.cleanup()

# Spustit poslech ve vlákně
button_thread = threading.Thread(target=listen_to_buttons)
button_thread.daemon = True
button_thread.start()

# Spuštění Flask aplikace (v hlavním vlákně!)
print("🚀 Flask API startuje...")
app = create_app()
app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
