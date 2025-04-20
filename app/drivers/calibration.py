import RPi.GPIO as GPIO
import time
from app.drivers.pins import Pins
from .step_motor import StepMotor
from .pins import Pins

class Calibration:
    def __init__(self,calibration_steps=535):  # Nový pin pro nový senzor


        self.calibration_steps = calibration_steps
        self.step_motor = StepMotor()

    def calibration_rotate(self):


        print("▶️ Spouštím kalibraci – otáčím krok po kroku...")
        self.step_motor.rotate_until_sensor()







