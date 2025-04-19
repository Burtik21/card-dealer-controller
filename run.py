# run.py
import RPi.GPIO as GPIO
import time
import requests
from app.drivers.pins import Pins
from app import create_app, Calibration

# Vytvoření Flask aplikace
app = create_app()
Pins.setup_pins()
calibration = Calibration()
calibration.calibration_rotate()

# Funkce pro odeslání požadavku na Node.js backend
def notify_node(button_index):
    try:
        response = requests.post(
            "http://localhost:3000/button-pressed",  # změň na IP, pokud je Node na jiném zařízení
            json={"button": button_index}
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_index} | Stav: {response.status_code}")
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
try:
    while True:
        for button in BUTTONS:
            if button.pin is not None and GPIO.input(button.pin) == GPIO.LOW:
                print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                notify_node(button.index)
                time.sleep(0.2)  # debounce
except KeyboardInterrupt:
    print("⛔ Ukončuji program.")
finally:
    GPIO.cleanup()

# Spuštění aplikace
if __name__ == "__main__":
    app.run(debug=True)
