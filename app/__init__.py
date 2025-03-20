from flask import Flask
from app.drivers.calibration import Calibration

def create_app():
    app = Flask(__name__)
    calibration = Calibration()
    calibration.calibration_rotate()
    return app
