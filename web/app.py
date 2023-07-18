from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# NB: when running this with docker compose then must use the service name 'api'
# not 'localhost'
API_PORT = os.environ.get("API_PORT", 8401)
BACKEND_URL = f"http://api:{API_PORT}"


@app.route('/')
def index():
    response = requests.get(f"{BACKEND_URL}/")
    return jsonify(response.json()), response.status_code

@app.route("/names/<string:name>")
def get_name(name):
    response = requests.get(f"{BACKEND_URL}/names/{name}")
    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8300, debug=True)
