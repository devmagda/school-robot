import RPi.GPIO as GPIO


class Pins:
    ACTIVE = False

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BOARD)
        Pins.ACTIVE = True
        return

    @staticmethod
    def close():
        GPIO.cleanup()


class Pin:
    def __init__(self, pin, value):
        if not Pins.ACTIVE:
            raise RuntimeError("Pins not initialized")
        self.pin = pin
        GPIO.setup(pin, value)


class Led(Pin):
    def __init__(self, pin):
        super().__init__(pin, GPIO.OUT)
        self.active = False

    def __del__(self):
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.active = True

    def deactivate(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.active = False

    def toggle(self):
        if self.active:
            self.deactivate()
        else:
            self.activate()


class Rotator(Pin):
    def __init__(self, pin):
        super().__init__(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)
        self.current_angle = 0

    def __del__(self):
        self.pwm.stop()

    def set_rotation(self, angle):
        if angle < 0 or angle > 180:
            raise ValueError('Angle out of range')
        self.current_angle = angle
        duty_cycle = self.calculate_duty_cycle()
        self.pwm.ChangeDutyCycle(duty_cycle)

    def add_rotation(self, angle):
        angle = self.current_angle + angle  # Pre calculate value
        self.set_rotation(angle)

    def calculate_duty_cycle(self):
        return 2.5 + (self.current_angle / 18)
