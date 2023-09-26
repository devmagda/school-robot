from flask import Flask, request, Response

from pi_controller import Controller

app = Flask(__name__)

conn = Controller()


@app.route('/rotation/add', methods=['GET'])
def add_rotation():
    # Get the two parameters from the URL query string
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    exit_code = 0
    try:
        conn.up(y)
    except ValueError:
        exit_code = 1
        print('Y Rotation invalid')
    try:
        conn.right(z)
    except ValueError:
        exit_code = 1
        print('Z Rotation invalid')
    if exit_code == 0:
        return Response(status=200)
    return Response(status=400)

@app.route('/rotation/set', methods=['GET'])
def set_rotation():
    # Get the two parameters from the URL query string
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    exit_code = 0
    try:
        conn.y_rotator.set_rotation(y)
    except ValueError:
        exit_code = 1
        print('Y Rotation invalid')
    try:
        conn.z_rotator.set_rotation(z)
    except ValueError:
        exit_code = 1
        print('Z Rotation invalid')
    if exit_code == 0:
        return Response(status=200)
    return Response(status=400)



# home route that returns below text
# when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


class Client:
    URL = "http://pi.local:8080"

    @staticmethod
    def add_rotation(z: int, y: int):
        Client.get(f'rotation/add/?z={z}&y={y}')

    @staticmethod
    def set_rotation(z: int, y: int):
        Client.get(f'rotation/set/?z={z}&y={y}')

    @staticmethod
    def get(endpoint):
        import requests
        response = requests.get(f'{Client.URL}/{endpoint}')
        if response.status_code != 200:
            raise ValueError('An Error occurred')


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
