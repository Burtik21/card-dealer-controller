import RPi.GPIO as GPIO
import time
from pins import Pins

class DCMotor:
    initialized = False

    @staticmethod
    def init():
        """ Inicializuje GPIO pouze jednou """
        if not DCMotor.initialized:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Pins.MOTOR_DC_IN1, GPIO.OUT)  # MOTOR_DC_IN1
            GPIO.setup(Pins.MOTOR_DC_IN2, GPIO.OUT)  # MOTOR_DC_IN2
            GPIO.setup(Pins.MOTOR_DC_PWM, GPIO.OUT)  # MOTOR_DC_PWM

            DCMotor.pwm_control = GPIO.PWM(Pins.MOTOR_DC_PWM, 1000)  # Frekvence 1kHz
            DCMotor.pwm_control.start(0)
            DCMotor.initialized = True

    @staticmethod
    def forward():
        """ Motor jede dopředu s danou rychlostí """
        DCMotor.init()
        GPIO.output(Pins.MOTOR_DC_IN1, GPIO.HIGH)
        GPIO.output(Pins.MOTOR_DC_IN2, GPIO.LOW)
        DCMotor.pwm_control.ChangeDutyCycle(100)

    @staticmethod
    def backward():
        """ Motor jede dozadu """
        DCMotor.init()
        GPIO.output(Pins.MOTOR_DC_IN1, GPIO.LOW)
        GPIO.output(Pins.MOTOR_DC_IN2, GPIO.HIGH)
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
        DCMotor.init()
        """ Uvolní GPIO """
        DCMotor.stop()
        DCMotor.pwm_control.stop()
        GPIO.cleanup()

    @staticmethod
    def deal_card():
        DCMotor.init()
        DCMotor.forward()
        time.sleep(0.03)
        DCMotor.stop()
        DCMotor.backward()
        time.sleep(0.01)
        DCMotor.stop()








