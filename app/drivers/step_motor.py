import RPi.GPIO as GPIO
import time
import threading
from .pins import Pins
from .dc_motor import DCMotor
import math

class StepMotor:
    _instance = None  # Uchovává jedinou instanci

    def __new__(cls, *args, **kwargs):
        """ Zajištění, že existuje pouze jedna instance """
        if cls._instance is None:
            cls._instance = super(StepMotor, cls).__new__(cls)
        return cls._instance

    def __init__(self, steps_per_rev=200, actual_steps=0, motor_direction=1,max_steps=200):
        """ Inicializace krokového motoru """

        if not hasattr(self, 'initialized'):
            self.lock = threading.Lock()
            self._stop_request = False
            self._actual_steps = actual_steps
            self._steps_per_rev = steps_per_rev
            self._motor_direction = motor_direction
            self._max_steps = max_steps
            self._motor_enabled = False
            self.initialized = True

    @property
    def motor_enabled(self):
        return

    @property
    def motor_direction(self):
        """ Getter pro směr motoru """
        return self._motor_direction

    @motor_direction.setter
    def motor_direction(self, direction):
        """ Nastavení směru: 1 = dopředu, 0 = zpět """
        self._motor_direction = direction
        GPIO.output(Pins.MOTOR_STEP_DIR, GPIO.HIGH if direction == 1 else GPIO.LOW)

    @property
    def actual_steps(self):
        return self._actual_steps

    @actual_steps.setter
    def actual_steps(self, steps):
        self._actual_steps = steps % 4280

    def rotate(self, steps, delay=0.0003):
        with self.lock:
            self._stop_request = False
            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.LOW)

            for i in range(steps+110):

                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                time.sleep(delay)

            time.sleep(0.3)
            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)

    def rotate_until_sensor(self, max_steps=4280, delay=0.0003):
        with self.lock:
            self._stop_request = False
            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.LOW)
            self.motor_direction = 1

            for step in range(max_steps):
                if GPIO.input(Pins.HALL_SENSOR) == GPIO.LOW:
                    print("✅ Hall senzor detekován.")
                    self._actual_steps = 0
                    self.motor_direction = 0
                    time.sleep(0.3)

                    for _ in range(10):
                        GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                        time.sleep(delay)
                        GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                        time.sleep(delay)

                    GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)
                    return True

                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                time.sleep(delay)

            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)
            print("⚠️ Hall senzor nenalezen po max krocích.")
            return False

    def stop_motor(self):
        print("🛑 Soft stop – vypínám ENABLE")
        GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)


    def cleanup(self):
        """ Vyčistí GPIO (ukončení programu) """
        GPIO.cleanup()
