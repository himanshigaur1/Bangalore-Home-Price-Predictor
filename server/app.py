from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)

# ✅ Allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    return jsonify({'locations': util.get_location_names()})

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.get_json()
    print("📥 Request Data:", data)

    try:
        total_sqft = float(data.get('total_sqft', 0))
        location = str(data.get('location', '')).strip()
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))
        print(f"✅ Inputs: sqft={total_sqft}, location={location}, bhk={bhk}, bath={bath}")

        estimated_price = util.get_estimated_price(total_sqft, location, bhk, bath)
        print("💰 Predicted Price:", estimated_price)
    except Exception as e:
        print("❌ Error:", e)
        estimated_price = 0

    return jsonify({'estimated_price': estimated_price})

if __name__ == "__main__":
    print("✅ Flask Server Running...")
    util.load_saved_artifacts()
    app.run(host="127.0.0.1", port=5000, debug=True)
