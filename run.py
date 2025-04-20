import RPi.GPIO as GPIO
import time
import threading
import queue
from flask import Flask, request, jsonify
from app.drivers.pins import Pins
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard

# === Nastavení GPIO ===
GPIO.setmode(GPIO.BCM)
Pins.setup_pins()

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

# === Inicializace motor komponent ===
calibration = Calibration()
deal_card = DealCard()

# === Fronta pro úkoly ===
motor_queue = queue.Queue()

# === Flask aplikace ===
app = Flask(__name__)

@app.route("/python/deal", methods=["POST"])
def api_deal():
    data = request.get_json()
    steps = data.get("steps")
    print(f"📤 Flask požadavek: vyhodit kartu ({steps} kroků)")
    motor_queue.put(("deal", steps))  # 🔁 NEVOLAT PŘÍMO motor!
    return jsonify({"status": "ok", "message": f"Zapsáno do fronty: {steps} kroků"})

@app.route("/python/calibrate", methods=["POST"])
def api_calibrate():
    print("📤 Flask požadavek: kalibrace")
    motor_queue.put(("calibrate", None))  # 🔁 Pouze vložit do fronty
    return jsonify({"status": "ok", "message": "Kalibrace zapsaná do fronty"})

# === Poslech tlačítek ve vlákně ===
def listen_to_buttons():
    try:
        print("▶️ Poslouchám tlačítka...")
        while True:
            for button in BUTTONS:
                if button.pin and GPIO.input(button.pin) == GPIO.LOW:
                    print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                    motor_queue.put(("deal", button.steps))
                    time.sleep(0.3)  # debounce
    except KeyboardInterrupt:
        print("⛔ Ukončuji poslech tlačítek.")
    finally:
        GPIO.cleanup()

# === Hlavní vlákno: zpracovává motorické úkoly ===
def main_motor_loop():
    print("🧠 Motor loop běží...")
    while True:
        task, value = motor_queue.get()
        if task == "deal":
            deal_card.deal(steps=value)
        elif task == "calibrate":
            calibration.calibration_rotate()

# === HLAVNÍ START ===
if __name__ == "__main__":
    print("🧭 Spouštím kalibraci při startu...")
    calibration.calibration_rotate()
    print("✅ Kalibrace hotová.")

    # Spustit Flask server ve vlákně
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False),
        daemon=True
    ).start()

    # Spustit poslech tlačítek ve vlákně
    threading.Thread(target=listen_to_buttons, daemon=True).start()

    # 🔁 Spustit hlavní smyčku (motor se točí vždy jen tady!)
    main_motor_loop()
