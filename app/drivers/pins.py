from .utils.button import Button
import RPi.GPIO as GPIO

class Pins:
    """ Třída pro definici všech GPIO pinů """
    # Krokový motor
    MOTOR_STEP_STEP = 22
    MOTOR_STEP_DIR = 27
    MOTOR_STEP_ENABLE = 4

    # DC motor (L298N)
    MOTOR_DC_IN1 = 6
    MOTOR_DC_IN2 = 5
    MOTOR_DC_PWM = 13

    M0= 11
    M1= 9

    HALL_SENSOR = 14 # Například pro senzor

    BUTTON_1 = Button(1, 1605, 1)
    BUTTON_2 = Button(2, 1070, 7)
    BUTTON_3 = Button(3, 535, 8)
    BUTTON_4 = Button(4, 3745, 25)
    BUTTON_5 = Button(5, 3210, 24)
    BUTTON_6 = Button(6, 2675, 23)

    @staticmethod
    def setup_pins():
        """Inicializace všech pinů"""
        GPIO.setmode(GPIO.BCM)  # BCM číslování
        GPIO.setup(Pins.MOTOR_STEP_STEP, GPIO.OUT)
        GPIO.setup(Pins.MOTOR_STEP_DIR, GPIO.OUT)
        GPIO.output(Pins.MOTOR_STEP_DIR, GPIO.HIGH)
        GPIO.setup(Pins.MOTOR_STEP_ENABLE, GPIO.OUT)
        GPIO.output(Pins.MOTOR_STEP_ENABLE, GPIO.LOW)
        GPIO.setup(Pins.MOTOR_DC_IN1, GPIO.OUT)
        GPIO.setup(Pins.MOTOR_DC_IN2, GPIO.OUT)
        GPIO.setup(Pins.MOTOR_DC_PWM, GPIO.OUT)
        GPIO.setup(Pins.HALL_SENSOR, GPIO.IN)

        GPIO.setup(Pins.M0, GPIO.OUT)
        GPIO.setup(Pins.M1, GPIO.OUT)
        GPIO.output(Pins.M1, GPIO.HIGH)
        GPIO.output(Pins.M0, GPIO.HIGH)



        print("GPIO piny byly úspěšně inicializovány!")




