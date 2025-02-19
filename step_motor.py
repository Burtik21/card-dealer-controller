import RPi.GPIO as GPIO
import time
from pins import Pins
from dc_motor import DCMotor

class StepMotor:
    def __init__(self, steps_per_rev=200):
        """ Inicializace krokového motoru """


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pins.MOTOR_STEP_STEP, GPIO.OUT)
        GPIO.setup(Pins.MOTOR_STEP_DIR, GPIO.OUT)

    def set_direction(self, direction):
        """ Nastavení směru: 1 = dopředu, 0 = zpět """
        GPIO.output(Pins.MOTOR_STEP_DIR, GPIO.HIGH if direction == 1 else GPIO.LOW)

    def rotate(self, steps, direction=1, delay=0.001):
        """ Otočení motoru:
        - rotations: počet otáček
        - direction: směr (1 = dopředu, 0 = zpět)
        - delay: čas mezi kroky (nižší = rychlejší otáčky) """
        self.set_direction(direction)


        for _ in range(steps):
            GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(Pins.MOTOR_STEP_STEP, GPIO.LOW)
            time.sleep(delay)



    def cleanup(self):
        """ Vyčistí GPIO (ukončení programu) """
        GPIO.cleanup()


