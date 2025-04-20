import threading
import queue
import RPi.GPIO as GPIO
import time
import requests
from flask import Flask
from app import create_app
from app.drivers.pins import Pins
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard

# === Příprava komponent ===
GPIO.setmode(GPIO.BCM)
Pins.setup_pins()

deal_card = DealCard()
calibration = Calibration()

# === Fronta pro motorové akce ===
motor_queue = queue.Queue()

# === Tlačítka ===
BUTTONS = [
    Pins.BUTTON_1,
    Pins.BUTTON_2,
    Pins.BUTTON_3,
    Pins.BUTTON_4,
    Pins.BUTTON_5,
    Pins.BUTTON_6,
]

for button in BUTTONS:
    if button.pin is not None:
        GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === Kalibrace při startu ===
print("🧭 Spouštím kalibraci...")
calibration.calibration_rotate()
print("✅ Kalibrace dokončena")

# === Posílání info o stisknutí tlačítka na Node.js backend (volitelné) ===
def notify_node(steps):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/deal",
            json={"steps": steps}
        )
        print(f"📤 Odesláno do Node.js: {steps} kroků | Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání: {e}")

# === Poslech tlačítek ve vlákně ===
def listen_to_buttons():
    try:
        print("▶️ Poslouchám tlačítka...")
        while True:
            for button in BUTTONS:
                if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                    print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                    motor_queue.put(("deal", button.steps))
                    time.sleep(0.3)
    except KeyboardInterrupt:
        print("⛔ Ukončuji poslech tlačítek.")
    finally:
        GPIO.cleanup()

# === Hlavní vlákno – vykonává úlohy (MOTOR!) ===
def motor_loop():
    while True:
        task, value = motor_queue.get()
        if task == "deal":
            deal_card.deal(steps=value)
        elif task == "calibrate":
            calibration.calibration_rotate()

# === Spustit tlačítka ve vlákně ===
threading.Thread(target=listen_to_buttons, daemon=True).start()

# === Spustit Flask ve vlákně ===
def start_flask():
    app = create_app(motor_queue)
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

threading.Thread(target=start_flask, daemon=True).start()

# === Tady běží motor – HLAVNÍ VLÁKNO ===
motor_loop()
