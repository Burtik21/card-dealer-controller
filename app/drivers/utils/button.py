class Button:
    def __init__(self, index, steps=0, pin=None):
        """
        Inicializace tlačítka
        :param index: index tlačítka (např. 0, 1, 2...)
        :param steps: počet kroků pro motor, který tento button spustí
        :param pin: GPIO pin pro tlačítko (volitelné, pokud je specifikováno)
        """
        self.index = index
        self.steps = steps
        self.pin = pin  # Volitelný GPIO pin pro tlačítko, pokud je třeba
