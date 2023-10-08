from threading import Thread

import requests

from pi.Logger import CustomLoggerPi

logger = CustomLoggerPi(__name__).get_logger()


class Client:
    URL = 'http://pi.local:8080/'

    BLOCK = False

    @staticmethod
    def add_rotation(z: int, y: int):
        if Client.BLOCK:
            logger.info(f'Blocked rotation {z}, {y}')
            pass
        else:
            Client.get_threaded(f'rotation/add?z={int(z)}&y={int(y)}', blocking=True)

    @staticmethod
    def set_rotation(z: int, y: int):
        if Client.BLOCK:
            pass
        else:
            Client.get_threaded(f'rotation/set?z={int(z)}&y={int(y)}', blocking=True)

    @staticmethod
    def shoot():
        Client.get_threaded('shoot')

    @staticmethod
    def get_threaded(endpoint, blocking=False):
        if blocking:
            Client.BLOCK = True
        Thread(target=Client.__get, args=(endpoint, blocking), daemon=True).start()

    @staticmethod
    def get(endpoint, blocking=False):
        Client.__get(endpoint, blocking)

    @staticmethod
    def __get(endpoint, disable_movement):
        path = f'{Client.URL}{endpoint}'
        # logger.info('RUNNING')
        try:
            # logger.info('Do request')
            requests.get(path, timeout=1)
            # logger.info('Did request')
        except:
            pass
            # logger.info('IO ERROR')
        if disable_movement:
            # logger.info('Got request')
            Client.BLOCK = False
