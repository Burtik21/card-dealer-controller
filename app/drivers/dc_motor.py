import RPi.GPIO as GPIO
import time
from .pins import Pins

class DCMotor:
    initialized = False

    @staticmethod
    def init():
        """ Inicializuje GPIO pouze jednou """
        if not DCMotor.initialized:

            DCMotor.pwm_control = GPIO.PWM(Pins.MOTOR_DC_PWM, 1000)  # Frekvence 1kHz
            DCMotor.pwm_control.start(0)
            DCMotor.initialized = True

    @staticmethod
    def forward():
        """ Motor jede dopředu s danou rychlostí """
        DCMotor.init()
        GPIO.output(Pins.MOTOR_DC_IN1, GPIO.LOW)
        GPIO.output(Pins.MOTOR_DC_IN2, GPIO.HIGH)
        DCMotor.pwm_control.ChangeDutyCycle(100)

    @staticmethod
    def backward():
        """ Motor jede dozadu """
        DCMotor.init()
        GPIO.output(Pins.MOTOR_DC_IN1, GPIO.HIGH)
        GPIO.output(Pins.MOTOR_DC_IN2, GPIO.LOW)
        DCMotor.pwm_control.ChangeDutyCycle(100)

    @staticmethod
    def stop():
        """ Motor se zastaví """
        DCMotor.init()
        GPIO.output(Pins.MOTOR_DC_IN1, GPIO.LOW)
        GPIO.output(Pins.MOTOR_DC_IN2, GPIO.LOW)
        DCMotor.pwm_control.ChangeDutyCycle(0)

    @staticmethod
    def cleanup():
        """ Uvolní GPIO – volat pouze při ukončení programu! """
        DCMotor.stop()
        DCMotor.pwm_control.stop()
        GPIO.cleanup()
        DCMotor.initialized = False  # ✅ Přidáno pro správnou reinicializaci

    @staticmethod
    def deal_card(forward_time=0.07,backward_time=0.035,wait_between=0.01 ):
        """ Ovládání motoru pro rozdání karty """
        time.sleep(0.5)
        DCMotor.init()
        DCMotor.forward()
        time.sleep(forward_time)
        DCMotor.stop()
        time.sleep(wait_between)
        DCMotor.backward()
        time.sleep(backward_time)
        DCMotor.stop()
