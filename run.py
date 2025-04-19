import threading
import RPi.GPIO as GPIO
import time
import requests
from app.drivers.pins import Pins
from app import create_app, Calibration




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

# Funkce pro odeslání požadavku na Node.js backend
def notify_node(button_index):
    try:
        response = requests.post(
            "http://localhost:3000/button-pressed",
            json={"button": button_index}
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_index} | Stav: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání do Node.js: {e}")

# Naslouchání tlačítkům ve vlákně
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

# Spuštění
if __name__ == "__main__":
    # Spustit naslouchání tlačítek ve vlákně
    threading.Thread(target=listen_to_buttons, daemon=True).start()
    app = create_app()
    # Spustit Flask app
    print("🚀 Flask API běží...")
    app.run(host="0.0.0.0", port=5001, debug=True)
