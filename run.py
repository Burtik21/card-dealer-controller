import threading
import RPi.GPIO as GPIO
import time
import requests
from app import create_app
from app.drivers.pins import Pins

Pins.setup_pins()

def notify_node(button_steps):
    try:
        response = requests.post(
            "http://localhost:5000/api/deal",
            json={"button_steps": button_steps}
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_steps} | Stav: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání do Node.js: {e}")

def listen_to_buttons():
    try:
        BUTTONS = [
            Pins.BUTTON_1,
            Pins.BUTTON_2,
            #Pins.BUTTON_3,
            Pins.BUTTON_4,
            Pins.BUTTON_5,
            Pins.BUTTON_6,
        ]

        for button in BUTTONS:
            if button.pin is not None:
                GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        print("▶️ Poslouchám tlačítka...")

        last_states = {btn.index: GPIO.HIGH for btn in BUTTONS}

        while True:
            for button in BUTTONS:
                if button.pin is not None:
                    current_state = GPIO.input(button.pin)
                    last_state = last_states[button.index]

                    if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                        print(f"🔘 Tlačítko {button.index} zmáčknuto!")
                        notify_node(button.index)

                    last_states[button.index] = current_state

            time.sleep(0.01)
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
