from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World! We're running full gas from a VSCode devcontainer"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8400, debug=True)
