import time

import RPi.GPIO as GPIO

from uln2003 import ULN2003


class Pin:
    def __init__(self, pin, value):
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


class SingleRotator:
    def __init__(self, pins=None, limits=(1000, -1000)):
        self.uln_controller = ULN2003(pins)
        self.steps_position = 0
        self.limit_upper, self.limit_lower = limits

    def set_rotation(self, steps=0):
        steps = steps - self.steps_position
        self.add_rotation(steps)

    def add_rotation(self, steps=0):
        temp_position = self.steps_position + steps
        # if temp_position <= self.limit_upper and temp_position >= self.limit_lower:
        self.steps_position = temp_position
        if steps != 0:
            self.uln_controller.step(n=steps)


class DualRotator(SingleRotator):
    def __init__(self, pins_left=None, pins_right=None, limits=(1000, -1000)):
        upper, lower = limits
        self.left = SingleRotator(pins_left, limits=limits)
        self.right = SingleRotator(pins_right, limits=(lower, upper))

    def set_rotation(self, steps=0):
        self.left.set_rotation(steps=steps)
        self.right.set_rotation(steps=-steps)

    def add_rotation(self, steps=0):
        self.left.add_rotation(steps=steps)
        self.right.add_rotation(steps=-steps)


class Controller:
    pins_y_left = (3, 5, 7, 9)
    pins_y_right = (17, 18, 23, 24)
    pins_z = (10, 11, 14, 15)

    pin_gun = 25  # GPIO Notation needed

    limits_z = (2000, -2000)
    limits_y = (500, -500)

    def __init__(self, dual=False):

        self.gun = Led(Controller.pin_gun)

        self.z = SingleRotator(
            pins=Controller.pins_z,
            limits=Controller.limits_z
        )

        if dual:
            self.y = DualRotator(
                pins_left=Controller.pins_y_left,
                pins_right=Controller.pins_y_right,
                limits=Controller.limits_y
            )
        else:
            self.y = SingleRotator(
                pins=Controller.pins_y_right,
                limits=Controller.limits_y
            )

    def shoot(self):
        self.gun.activate()
        time.sleep(1)
        self.gun.deactivate()

    def up(self, angle):
        self.y.add_rotation(angle)

    def down(self, angle):
        self.y.add_rotation(-angle)

    def left(self, angle):
        self.z.add_rotation(angle)

    def right(self, angle):
        self.z.add_rotation(-angle)

    def __get_single_step(self, steps):
        if steps > 0:
            return int(1)
        if steps < 0:
            return int(-1)
        return int(0)

    def set(self, z, y):
        steps_z = z - self.z.steps_position
        steps_y = y - self.y.steps_position
        self.move(steps_z, steps_y)

    def move(self, z, y):
        loop_counter = 0
        if abs(z) >= abs(y):
            loop_size = abs(z)
        else:
            loop_size = abs(y)

        step_z = self.__get_single_step(z)
        step_y = self.__get_single_step(y)

        while loop_size >= loop_counter:
            loop_counter = loop_counter + 1
            if loop_counter <= abs(y):
                self.up(step_y)
            if loop_counter <= abs(z):
                self.right(step_z)

    def __del__(self):
        self.z.set_rotation(steps=0)
        self.y.set_rotation(steps=0)
        GPIO.cleanup()
