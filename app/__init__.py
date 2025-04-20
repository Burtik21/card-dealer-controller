from flask import Flask, request, jsonify
from app.drivers.calibration import Calibration
from app.drivers.deal_card import DealCard
from app.drivers.pins import Pins


def create_app():
    app = Flask(__name__)

    # Inicializace instancí
    deal_card = DealCard()
    calibration = Calibration()

    @app.route("/python/deal", methods=["POST"])
    def api_deal():
        data = request.get_json()
        steps = data.get("steps")

        if steps is None:
            return jsonify({"status": "error", "message": "Chybí 'steps'"}), 400

        print(f"📤 API požadavek: vyhodit kartu ({steps} kroků)")

        # ✅ PŘÍMO zavolat deal – bez vláken
        deal_card.deal(steps=steps)

        return jsonify({"status": "ok", "message": f"Dealt {steps} steps"})

    @app.route("/python/calibrate", methods=["POST"])
    def api_calibrate():
        print("📤 API požadavek: kalibrace")

        # ✅ PŘÍMO zavolat kalibraci – bez vláken
        calibration.calibration_rotate()

        return jsonify({"status": "ok", "message": "Kalibrace dokončena"})

    return app
