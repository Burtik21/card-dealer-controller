import time

from step_motor import StepMotor
from dc_motor import DCMotor

class MotorManager:
    def __init__(self):
        self.running = True  # ✅ Musí být uvnitř __init__
        self.step_motor = StepMotor()  # ✅ Vytvoření instance motoru

    def run(self):
        """ Hlavní smyčka programu """
        while self.running:
            try:
                deal_direction = input("Zadej uhel vyhození karty (stupně): ")
                steps = int(deal_direction)

                self.step_motor.rotate(steps)
                DCMotor.deal_card(0.073,0.045,0.015)

            except ValueError:
                print("⚠️ Zadali jste neplatnou hodnotu, zkuste to znovu.")

            except KeyboardInterrupt:
                print("\nUkončuji program...")
                self.running = False
                DCMotor.cleanup()
                self.step_motor.cleanup()

    def run2(self):
        """ Hlavní smyčka programu """
        global forward_time
        global backward_time
        global between_time
        global first
        first = False
        while self.running:
            try:

                #deal_direction = input("Zadej uhel vyhození karty (stupně): ")
                #steps = int(deal_direction)

                #self.step_motor.rotate(steps)
                if first:
                    again = int(input("znovu to stejne?"))
                    if again == 1:
                        DCMotor.deal_card(forward_time / 1000, backward_time / 1000, between_time / 1000)
                        first = True
                    elif again == 2:
                        forward_time = int(input("zadej delku toceni v pred"))
                        backward_time = int(input("zadej delku toceni v zad"))
                        between_time = int(input("zadej delku mezi"))
                        DCMotor.deal_card(forward_time / 1000, backward_time / 1000, between_time / 1000)
                        first = True
                elif first == False:
                    forward_time = int(input("zadej delku toceni v pred"))
                    backward_time = int(input("zadej delku toceni v zad"))
                    between_time = int(input("zadej delku mezi"))
                    DCMotor.deal_card(forward_time / 1000, backward_time / 1000, between_time / 1000)
                    first = True




            except ValueError:
                print("⚠️ Zadali jste neplatnou hodnotu, zkuste to znovu.")

            except KeyboardInterrupt:
                print("\nUkončuji program...")
                self.running = False
                DCMotor.cleanup()
                self.step_motor.cleanup()

    def run3(self):
        """ Hlavní smyčka programu """
        while self.running:
            try:
                deal_direction = input("Zadej uhel vyhození karty (stupně): ")
                steps = int(deal_direction)

                self.step_motor.rotate(steps)
                time.sleep(4)
                DCMotor.deal_card(0.055,0.030,0.015)

            except ValueError:
                print("⚠️ Zadali jste neplatnou hodnotu, zkuste to znovu.")

            except KeyboardInterrupt:
                print("\nUkončuji program...")
                self.running = False
                DCMotor.cleanup()
                self.step_motor.cleanup()


manager = MotorManager()# Vytvoří instanci
selection = int(input("otaceni (1) vyhazovani karet (2) otoceni a vyhozeni (3)"))
if selection == 1:
    manager.run()  # Spustí hlavní smyčku
elif selection == 2:
    manager.run2()
elif selection == 3:
    manager.run3()
