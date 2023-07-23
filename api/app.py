from fastapi import FastAPI
import requests
import json

# Create the app
app = FastAPI()

# Define the route
@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/names/{name}")
def names(name: str):
    return {"Your name is": name}


@app.get("/discharges/predictions")
def discharges_predictions():
    """
    Returns a list of discharge predictions.
    http://uclvlddpragae08:5691/predictions/
    ```
        [
        {
            "event_timestamp": "2023-07-22T19:04:57",
            "note": "foo bar",
            "discharge_probability": 1.0
        },
        ...
        ]
    ```
    """
    try:
        response = requests.get("http://uclvlddpragae08:5691/predictions")
        data = response.json()
    except requests.exceptions.ConnectionError as e:
        print(e)
        print("Will try with local data")
        with open("data/test/discharges.json") as f:
            data = json.load(f)
    return data

