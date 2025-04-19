import threading
import RPi.GPIO as GPIO
import time
import requests
from app.drivers.pins import Pins
from app import create_app, Calibration






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

        print("▶️ Poslouchám tlačítka...")

        # Uložíme si stav posledního přečtení
        last_states = {btn.index: GPIO.HIGH for btn in BUTTONS}

        while True:
            for button in BUTTONS:
                if button.pin is not None:
                    current_state = GPIO.input(button.pin)
                    last_state = last_states[button.index]

                    if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                        print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                        notify_node(button.index)

                    # Uložíme nový stav
                    last_states[button.index] = current_state

            time.sleep(0.01)  # rychlej polling
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
