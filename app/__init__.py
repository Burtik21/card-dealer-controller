from flask import Flask, request, jsonify
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard
from app.drivers.pins import Pins
import threading


def create_app():
    app = Flask(__name__)
    deal_card = DealCard()
    calibration = Calibration()


    @app.route("/python/deal", methods=["POST"])
    def api_deal():
        data = request.get_json()
        steps = data.get("steps")

        if steps is None:
            return jsonify({"status": "error", "message": "Chybí 'steps'"}), 400

        print(f"📤 API požadavek: vyhodit kartu ({steps} kroků)")

        # 🚀 Spustit v novém vlákně
        threading.Thread(target=lambda: deal_card.deal(steps=steps)).start()

        return jsonify({"status": "ok", "message": f"Dealing {steps} steps..."})

    @app.route("/python/calibrate", methods=["POST"])
    def api_calibrate():
        print("📤 API požadavek: kalibrace")
        threading.Thread(target=calibration.calibration_rotate).start()
        return jsonify({"status": "ok", "message": "Kalibrace zahájena"})

    return app
