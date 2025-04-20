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
        # Nastavení jednotlivých pinů
        BUTTON1 = Pins.BUTTON_1.pin
        BUTTON2 = Pins.BUTTON_2.pin
        BUTTON4 = Pins.BUTTON_4.pin
        BUTTON5 = Pins.BUTTON_5.pin
        BUTTON6 = Pins.BUTTON_6.pin

        buttons = [BUTTON1, BUTTON2, BUTTON4, BUTTON5, BUTTON6]
        for pin in buttons:
            if pin is not None:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        print("▶️ Jednoduchý režim naslouchání tlačítkům...")

        # Čas posledního stisknutí pro každý pin
        last_pressed = {
            BUTTON1: 0,
            BUTTON2: 0,
            BUTTON4: 0,
            BUTTON5: 0,
            BUTTON6: 0,
        }

        cooldown = 3  # sekundy

        while True:
            now = time.time()

            if BUTTON1 is not None and GPIO.input(BUTTON1) == GPIO.LOW:
                if now - last_pressed[BUTTON1] > cooldown:
                    print("🔘 Tlačítko 1 zmáčknuto")
                    notify_node(1)
                    last_pressed[BUTTON1] = now

            if BUTTON2 is not None and GPIO.input(BUTTON2) == GPIO.LOW:
                if now - last_pressed[BUTTON2] > cooldown:
                    print("🔘 Tlačítko 2 zmáčknuto")
                    notify_node(2)
                    last_pressed[BUTTON2] = now

            if BUTTON4 is not None and GPIO.input(BUTTON4) == GPIO.LOW:
                if now - last_pressed[BUTTON4] > cooldown:
                    print("🔘 Tlačítko 4 zmáčknuto")
                    notify_node(4)
                    last_pressed[BUTTON4] = now

            if BUTTON5 is not None and GPIO.input(BUTTON5) == GPIO.LOW:
                if now - last_pressed[BUTTON5] > cooldown:
                    print("🔘 Tlačítko 5 zmáčknuto")
                    notify_node(5)
                    last_pressed[BUTTON5] = now

            if BUTTON6 is not None and GPIO.input(BUTTON6) == GPIO.LOW:
                if now - last_pressed[BUTTON6] > cooldown:
                    print("🔘 Tlačítko 6 zmáčknuto")
                    notify_node(6)
                    last_pressed[BUTTON6] = now

            time.sleep(0.05)  # Rychlej polling, ale se zpožděním
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
