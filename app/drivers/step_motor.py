import RPi.GPIO as GPIO
import time
import threading
from pins import Pins
from dc_motor import DCMotor

class StepMotor:
    def __init__(self, steps_per_rev=200):
        """ Inicializace krokového motoru """

        self.lock = threading.Lock()
        self.stop_request = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pins.MOTOR_STEP_STEP, GPIO.OUT)
        GPIO.setup(Pins.MOTOR_STEP_DIR, GPIO.OUT)

    def set_direction(self, direction):
        """ Nastavení směru: 1 = dopředu, 0 = zpět """
        GPIO.output(Pins.MOTOR_STEP_DIR, GPIO.HIGH if direction == 1 else GPIO.LOW)

    def rotate(self, steps, direction=1, delay=0.001):
        self.set_direction(direction)

        with self.lock:
            self.stop_request = False
            for _ in range(steps):
                if self.stop_request == False:
                    GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                    time.sleep(delay)
                else:
                    print("motor zastaven")
            time.delay(0.5)

    def stop_motor(self):
        print("stop prijat")
        self.stop_request = True
        time.delay(5)
        self.stop_request = False


    def cleanup(self):
        """ Vyčistí GPIO (ukončení programu) """
        GPIO.cleanup()


