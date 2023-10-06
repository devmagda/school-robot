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
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    conn.move(z, y)
    return Response(status=200)


@app.route('/rotation/set', methods=['GET'])
def set_rotation():
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    conn.set(z, y)
    return Response(status=200)


@app.route('/shoot')
def shoot():
    conn.shoot()
    return Response(status=200)


# home route that returns below text
# when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
