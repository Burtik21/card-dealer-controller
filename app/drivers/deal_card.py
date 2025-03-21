import threading

import RPi.GPIO as GPIO
import time
from app.drivers.pins import Pins
from step_motor import StepMotor
from pins import Pins
from dc_motor import DCMotor

class DealCard():
    def __init__(self):
        self.lock = threading.Lock()
        self.step_motor = StepMotor()
        self.dc_motor = DCMotor()


    def deal(self,button=None,steps=None, number_of_cards=1):
        with self.lock:
            if (button is not None) and (steps is not None):
                raise ValueError("Můžeš zadat buď 'button' nebo 'steps', ale ne obojí zároveň!")
            if (button is None) and (steps is None):
                raise ValueError("Musíš zadat buď 'button' nebo 'steps'!")

            if button is not None:
                button.
                self.step_motor.rotate()

    def find_shortest_path(self,absolute_deal_steps):
        """
        absolute_steps = kroky od nuloveho bodu (buttonu nebo proste misto kam chceme vyhodit kartu)
        steps = kolik kroku ma udelat
        """
        cw=(self.step_motor.actual_steps-absolute_deal_steps)%200
        anti_cw=(absolute_deal_steps-self.step_motor.actual_steps)%200

        if anti_cw < cw:
            self.step_motor.motor_direction = 1
        else:
            self.step_motor.motor_direction = 0

