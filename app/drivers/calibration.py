import RPi.GPIO as GPIO
import time
from app.drivers.pins import Pins
from .step_motor import StepMotor
from .pins import Pins

class Calibration:
    def __init__(self,calibration_state=False,calibration_steps=535):  # Nový pin pro nový senzor

        self.calibration_state = calibration_state
        self.calibration_steps = calibration_steps
        self.step_motor = StepMotor()

    def calibration_rotate(self):
        if self.calibration_state:
            return 1

        print("▶️ Spouštím kalibraci – otáčím krok po kroku...")
        nalezeno = self.step_motor.rotate_until_sensor(max_steps=self.calibration_steps)

        if nalezeno:
            self.calibration_state = True
            self.step_motor.stop_motor()
            print("✅ Kalibrace hotová, motor zastaven.")
        else:
            print("❌ Kalibrace selhala – Hall senzor nenalezen.")






