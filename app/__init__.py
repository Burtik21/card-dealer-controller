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
        print(f"📤 API požadavek: vyhodit kartu ({steps} kroků)")
        motor_queue.put(("deal", steps))  # 💥 místo přímého volání
        return jsonify({"status": "ok"})

    @app.route("/python/calibrate", methods=["POST"])
    def api_calibrate():
        print("📤 API požadavek: kalibrace")
        motor_queue.put(("calibrate", None))  # 💥 taky jen přidat do fronty
        return jsonify({"status": "ok"})

    return app
