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

# === Inicializace motor komponent ===
calibration = Calibration()
deal_card = DealCard()

# === Fronta pro úkoly ===
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

# === Flask aplikace ===
app = Flask(__name__)

@app.route("/python/deal", methods=["POST"])
def api_deal():
    data = request.get_json()
    steps = data.get("steps")
    print(f"📤 Flask požadavek: vyhodit kartu ({steps} kroků)")
    motor_queue.put(("deal", steps))
    return jsonify({"status": "ok", "message": f"Zapsáno do fronty: {steps} kroků"})

@app.route("/python/calibrate", methods=["POST"])
def api_calibrate():
    print("📤 Flask požadavek: kalibrace")
    motor_queue.put(("calibrate", None))
    return jsonify({"status": "ok", "message": "Kalibrace zapsaná do fronty"})

# === Poslech tlačítek ve vlákně ===
def listen_to_buttons():
    print("▶️ Poslouchám tlačítka...")
    try:
        last_press_time = time.time()
        cooldown = 0.5  # debounce mezi stisky

        while True:
            for button in BUTTONS:
                if button.pin and GPIO.input(button.pin) == GPIO.LOW:
                    now = time.time()
                    if now - last_press_time > cooldown:
                        print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                        motor_queue.put(("deal", button.steps))
                        last_press_time = now
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()

# === Hlavní spuštění ===
if __name__ == "__main__":
    print("🧭 Spouštím počáteční kalibraci...")
    calibration.calibration_rotate()
    print("✅ Kalibrace hotová.")

    # Spuštění Flask serveru ve vlákně
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False),
        daemon=True
    ).start()

    # Spuštění poslechu tlačítek ve vlákně
    threading.Thread(target=listen_to_buttons, daemon=True).start()

    # 🔁 Hlavní zpracování motorových příkazů
    print("🧠 Hlavní smyčka motoru běží...")
    while True:
        task, value = motor_queue.get()
        if task == "deal":
            print(f"➡️ Spouštím DEAL ({value} kroků)")
            deal_card.deal(steps=value)
        elif task == "calibrate":
            print("➡️ Spouštím KALIBRACI")
            calibration.calibration_rotate()
        time.sleep(0.01)
