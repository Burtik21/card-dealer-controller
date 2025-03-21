from app.drivers import deal_card
from app.drivers.calibration import Calibration
from app.drivers.pins import Pins
from app.drivers.step_motor import StepMotor
from app.drivers.dc_motor import DCMotor
from app.drivers.deal_card import DealCard
def run():
    # Inicializace všech komponent
    Pins.setup_pins()
    calibration = Calibration()
    step_motor = StepMotor()
    dc_motor = DCMotor()
    deal_card = DealCard()


    # Mapa (slovník) pro propojení akce s metodou
    actions = {
        1: calibration.calibration_rotate,
        2: lambda: rotate_motor(step_motor),
        3: step_motor.stop_motor,
        4: dc_motor.deal_card,
        5: deal_card.deal(300),
        6: display_help,
        7: exit_app
    }

    # Menu pro uživatele
    menu = """
    Vyber akci:
    1. Kalibrace
    2. Otáčet motor
    3. Zastavit motor
    4. Vyhodit kartu
    5. deal karty
    6. Zobrazit nápovědu
    7. Ukončit
    """

    while True:
        print(menu)
        try:
            choice = int(input("Zadej číslo akce (1-6): ").strip())

            # Pokud volba existuje v mapě, zavolej metodu
            if choice in actions:
                actions[choice]()  # Zavolání příslušné metody
            else:
                print("Neplatná volba, zadejte číslo mezi 1 a 6.")

        except ValueError:
            print("Neplatný vstup, zadejte číslo.")

# Pomocné metody
def rotate_motor(step_motor):
    print("Zadej počet kroků pro otáčení:")
    steps = int(input().strip())
    print("Zadej směr (1 pro dopředu, 0 pro zpět):")
    direction = int(input().strip())
    print(f"Otáčím motor o {steps} kroků, směr: {'dopředu' if direction == 1 else 'zpět'}")
    step_motor.rotate(steps, direction)

def display_help():
    print("""
    Vyber akci:
    1. Kalibrace
    2. Otáčet motor
    3. Zastavit motor
    4. Vyhodit kartu
    5. deal karty
    6. Zobrazit nápovědu
    7. Ukončit
    """)

def exit_app():
    print("Ukončuji aplikaci.")
    exit(0)

if __name__ == '__main__':
    run()
