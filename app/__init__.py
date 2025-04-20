from flask import Flask, request, jsonify
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard
from app.drivers.pins import Pins

def create_app():
    app = Flask(__name__)


    deal_card = DealCard()

    @app.route("/python/deal", methods=["POST"])
    def api_deal():
        data = request.get_json()
        steps = data.get("steps")  # default hodnota
        print(f"📤 API požadavek: vyhodit kartu ({steps} kroků)")
        deal_card.deal(steps=steps)
        return jsonify({"status": "ok", "message": f"Dealt {steps} steps"})

    @app.route("/python/calibrate", methods=["POST"])
    def api_calibrate():
        print("📤 API požadavek: kalibrace")
        calibration.calibration_rotate()
        return jsonify({"status": "ok", "message": "Kalibrace dokončena"})

    return app
