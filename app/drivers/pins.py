from .utils.button import Button
class Pins:
    """ Třída pro definici všech GPIO pinů """
    # Krokový motor
    MOTOR_STEP_STEP = 22
    MOTOR_STEP_DIR = 27

    # DC motor (L298N)
    MOTOR_DC_IN1 = 6
    MOTOR_DC_IN2 = 5
    MOTOR_DC_PWM = 13

    HALL_SENSOR = 24  # Například pro senzor

    BUTTON_1 = Button(1,0,0)
    BUTTON_2 = Button(2,0,0)
    BUTTON_3 = Button(3,0,0)
    BUTTON_4 = Button(4,0,0)
    BUTTON_5 = Button(5,0,0)
    BUTTON_6 = Button(6,0,0)




