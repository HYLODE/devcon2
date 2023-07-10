from fastapi import FastAPI

# Create the app
app = FastAPI()

# Define the route
@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/names/{name}")
def names(name: str):
    return {"Your name is": name}

