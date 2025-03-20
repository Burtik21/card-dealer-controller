import RPi.GPIO as GPIO
from app.drivers.pins import Pins
from app.drivers.step_motor import StepMotor

class ZeroPoint:
    def __init__(self,calibration_state=False,calibration_steps=400):
        self.pin_number = Pins.HALL_SENSOR  # Nový pin pro nový senzor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.IN)
        self.calibration_state = calibration_state
        self.calibration_steps = calibration_steps
        self.step_motor = StepMotor

    def calibration_rotate(self):
        if self.calibration_state:
            self.calibration_state=True
            return 1
        else:
            self.step_motor.rotate(self.calibration_steps)
            while GPIO.input(self.pin_number) == GPIO.HIGH:



