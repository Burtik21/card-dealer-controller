import RPi.GPIO as GPIO
import time
from app.drivers.pins import Pins
from .step_motor import StepMotor
from .pins import Pins

class Calibration:
    def __init__(self,calibration_state=False,calibration_steps=400):  # Nový pin pro nový senzor

        self.calibration_state = calibration_state
        self.calibration_steps = calibration_steps
        self.step_motor = StepMotor()

    def calibration_rotate(self):
        if self.calibration_state:
            return 1
        else:
            start_time = time.time()  # Uložíme čas startu pro timeout
            timeout = 10
            self.step_motor.rotate(self.calibration_steps)
            while time.time() - start_time < timeout:
                print("hledame nulovy bod")
                if GPIO.input(Pins.HALL_SENSOR) == GPIO.LOW:
                    self.calibration_state = True
                    self.step_motor.stop_motor()
                    self.step_motor.actual_steps = 0
                    GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.HIGH)
                    return





