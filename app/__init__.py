from flask import Flask
from .drivers import zero_point

def create_app():
    app = Flask(__name__)

    return app
