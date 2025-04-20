from flask import Flask, request, jsonify
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard
from app.drivers.pins import Pins


def create_app(motor_queue):
    app = Flask(__name__)

    @app.route("/python/deal", methods=["POST"])
    def api_deal():
        data = request.get_json()
        steps = data.get("steps")
        motor_queue.put(("deal", steps))
        return jsonify({"status": "ok"})

    @app.route("/python/calibrate", methods=["POST"])
    def api_calibrate():
        motor_queue.put(("calibrate", None))
        return jsonify({"status": "ok"})

    return app

