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
                DCMotor.deal_card()

            except ValueError:
                print("⚠️ Zadali jste neplatnou hodnotu, zkuste to znovu.")

            except KeyboardInterrupt:
                print("\nUkončuji program...")
                self.running = False
                DCMotor.cleanup()
                self.step_motor.cleanup()


manager = MotorManager()  # Vytvoří instanci
manager.run()  # Spustí hlavní smyčku
