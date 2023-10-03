from flask import Flask, request, Response

from pi_controller import Controller

app = Flask(__name__)

conn = Controller()

"""
in5 = 5
in6 = 0
in7 = 11
in8 = 9

GPIO.setmode( GPIO.BCM )
GPIO.setup( in5, GPIO.OUT )
GPIO.setup( in6, GPIO.OUT )
GPIO.setup( in7, GPIO.OUT )
GPIO.setup( in8, GPIO.OUT )

# initializing
GPIO.output( in5, GPIO.LOW )
GPIO.output( in6, GPIO.LOW )
GPIO.output( in7, GPIO.LOW )
GPIO.output( in8, GPIO.LOW )

motor_pins = [in5,in6,in7,in8]
motor_step_counter = 0 ;
"""
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
    else:
        return Response(status=400)

@app.route('/rotation/set', methods=['GET'])
def set_rotation():
    exit_code = 0

    # Get the two parameters from the URL query string
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))

    try:
        conn.y.set_rotation(steps=y)
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
    else:
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
        if response.status_code == 400:
            raise ValueError('Could not do action!')


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
