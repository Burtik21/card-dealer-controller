from flask import Flask
from app.drivers.calibration import Calibration
from app.drivers.pins import Pins

def create_app():
    app = Flask(__name__)
    Pins.setup_pins()
    calibration = Calibration()
    calibration.calibration_rotate()
    return app
