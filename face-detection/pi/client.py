import requests


class Client:
    URL = "http://pi.local:8080"

    @staticmethod
    def add_rotation(z: int, y: int):
        Client.get(f'rotation/add/?z={z}&y={y}')

    @staticmethod
    def set_rotation(z: int, y: int):
        Client.get(f'rotation/set/?z={z}&y={y}')

    @staticmethod
    def shoot():
        Client.get('shoot')

    @staticmethod
    def get(endpoint):
        response = requests.get(f'{Client.URL}/{endpoint}')
        if response.status_code == 400:
            raise ValueError('Could not do action!')
