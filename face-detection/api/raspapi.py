from fastapi import FastAPI

from api.controller import Rotator, Led, Pins

app = FastAPI()

Pins.init()

z_rotator = Rotator(pin=15)
y_rotator = Rotator(pin=16)
laser = Led(pin=25)


# /rotation/set/?z=5&y=7
@app.get("/rotation/set/")
def set_rotation(z: int, y: int):
    try:
        z_rotator.set_rotation(z)
        y_rotator.set_rotation(y)
        return {"result": True}
    except ValueError:
        return {"result": False}


# /rotation/add/?z=5&y=7
@app.get("/rotation/add/")
def add_rotation(z: int, y: int):
    try:
        z_rotator.set_rotation(z)
        y_rotator.set_rotation(y)
        return {"result": True}
    except ValueError:
        return {"result": False}


class Client:
    URL = "http://pi.local:8001"

    @staticmethod
    def add_rotation(z: int, y: int):
        Client.get(f'/rotation/add/?z={z}&y={y}')

    @staticmethod
    def set_rotation(z: int, y: int):
        Client.get(f'/rotation/set/?z={z}&y={y}')

    @staticmethod
    def get(endpoint):
        import requests
        response = requests.get(f'{Client.URL}{endpoint}')
        if response.status_code != 200:
            raise ValueError('An Error occurred')

