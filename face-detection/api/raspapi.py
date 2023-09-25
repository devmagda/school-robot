from flask import Flask, request

from pi_controller import Controller

app = Flask(__name__)

conn = Controller()


@app.route('/rotation/add', methods=['GET'])
def add_numbers():
    # Get the two parameters from the URL query string
    y = request.args.get('y')
    z = request.args.get('z')
    conn.up(y)
    conn.right(z)


# home route that returns below text
# when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(host='169.254.160.151', debug=True, port=8080)
