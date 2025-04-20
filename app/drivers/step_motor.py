import RPi.GPIO as GPIO
import time
import threading
from .pins import Pins
import math
from .dc_motor import DCMotor


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
        if (self._actual_steps + steps) > 535:
            self._actual_steps = steps - 535
        else:
            self._actual_steps += steps

    def rotate(self, steps, delay=0.001):
        with self.lock:
            self._stop_request = False

            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.LOW)

            ramp_steps = min(20, steps)  # prvních 20 kroků zpomalíme
            start_delay = 0.005  # pomalý start (větší delay)
            end_delay = delay  # cílová rychlost

            for i in range(steps):
                if self._stop_request:
                    print("motor zastaven")
                    break

                # Výpočet delay (lineární ramp-up)
                if i < ramp_steps:
                    current_delay = start_delay - ((start_delay - end_delay) * (i / ramp_steps))
                else:
                    current_delay = end_delay

                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                time.sleep(current_delay)
                GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                time.sleep(current_delay)

            time.sleep(0.5)
            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)

    import math

    def rotate_until_sensor(self, max_steps=1000, delay=0.001):
        with self.lock:
            self._stop_request = False
            GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.LOW)
            self.motor_direction = 1

            for step in range(max_steps):
                if GPIO.input(Pins.HALL_SENSOR) == GPIO.LOW:
                    print("✅ Hall senzor detekován.")
                    self._actual_steps = 0
                    self.motor_direction = 0
                    time.sleep(0.5)

                    # Exponenciální ramp-up na 55 kroků
                    total_steps = 55
                    ramp_steps = total_steps
                    start_delay = 0.008
                    end_delay = delay

                    for i in range(total_steps):
                        # 🧠 Exponenciální přechod delaye (větší plynulost)
                        t = i / ramp_steps
                        current_delay = start_delay * math.exp(-3 * t) + end_delay * (1 - math.exp(-3 * t))

                        GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
                        time.sleep(current_delay)
                        GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
                        time.sleep(current_delay)

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
