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
            json={"steps": button_steps}  # ← TADY!
        )
        print(f"📤 Odesláno do Node.js: tlačítko {button_steps} | Stav: {response.status_code}")
    except Exception as e:
        print(f"❌ Chyba při odesílání do Node.js: {e}")

def listen_to_buttons():
    try:
        # PINY
        BUTTON1 = Pins.BUTTON_1.pin
        BUTTON2 = Pins.BUTTON_2.pin
        BUTTON4 = Pins.BUTTON_4.pin
        BUTTON5 = Pins.BUTTON_5.pin
        BUTTON6 = Pins.BUTTON_6.pin

        pins = [BUTTON1, BUTTON2, BUTTON4, BUTTON5, BUTTON6]
        for pin in pins:
            if pin is not None:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        print("▶️ Naslouchání tlačítkům (s cooldownem + stabilitou)...")

        # Stav posledního zmáčknutí
        last_pressed = {pin: 0 for pin in pins}
        cooldown = 3  # sekundy

        while True:
            now = time.time()

            if BUTTON1 and GPIO.input(BUTTON1) == GPIO.LOW and now - last_pressed[BUTTON1] > cooldown:
                time.sleep(0.02)  # anti-bounce check
                if GPIO.input(BUTTON1) == GPIO.LOW:
                    print("🔘 Tlačítko 1 zmáčknuto")
                    notify_node(1)
                    last_pressed[BUTTON1] = now

            if BUTTON2 and GPIO.input(BUTTON2) == GPIO.LOW and now - last_pressed[BUTTON2] > cooldown:
                time.sleep(0.02)
                if GPIO.input(BUTTON2) == GPIO.LOW:
                    print("🔘 Tlačítko 2 zmáčknuto")
                    notify_node(2)
                    last_pressed[BUTTON2] = now

            if BUTTON4 and GPIO.input(BUTTON4) == GPIO.LOW and now - last_pressed[BUTTON4] > cooldown:
                time.sleep(0.02)
                if GPIO.input(BUTTON4) == GPIO.LOW:
                    print("🔘 Tlačítko 4 zmáčknuto")
                    notify_node(4)
                    last_pressed[BUTTON4] = now

            if BUTTON5 and GPIO.input(BUTTON5) == GPIO.LOW and now - last_pressed[BUTTON5] > cooldown:
                time.sleep(0.02)
                if GPIO.input(BUTTON5) == GPIO.LOW:
                    print("🔘 Tlačítko 5 zmáčknuto")
                    notify_node(5)
                    last_pressed[BUTTON5] = now

            if BUTTON6 and GPIO.input(BUTTON6) == GPIO.LOW and now - last_pressed[BUTTON6] > cooldown:
                time.sleep(0.02)
                if GPIO.input(BUTTON6) == GPIO.LOW:
                    print("🔘 Tlačítko 6 zmáčknuto")
                    notify_node(6)
                    last_pressed[BUTTON6] = now

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
