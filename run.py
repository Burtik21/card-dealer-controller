import threading
import RPi.GPIO as GPIO
import time
import requests
from app import create_app
from app.drivers.pins import Pins



def notify_node(button_steps):
    try:
        response = requests.post(
            "http://localhost:5000/api/deal",
            json={"steps": button_steps}  # ← TADY!
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_steps} | Stav: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání do Node.js: {e}")


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
        while True:
            for button in BUTTONS:
                if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                    print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                    notify_node(button.index)
                    time.sleep(0.2)  # debounce
    except KeyboardInterrupt:
        print("⛔ Ukončuji poslech tlačítek.")
    finally:
        GPIO.cleanup()


# 🧠 Teď spustíme hlavní část
if __name__ == "__main__":
    # Spusť GPIO poslech dřív, než se vytvoří app
    threading.Thread(target=listen_to_buttons, daemon=True).start()

    # Teprve teď vytvoř Flask app (která taky může používat GPIO)
    app = create_app()

    # Flask API start
    print("🚀 Flask API běží...")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
