from pi.pi_controller import Led
from pi.uln2003 import ULN2003


class RangeDetector:
    def __init__(self, pin_1, pin_n):
        pass

    def get_range(self) -> float:
        return float(10)


class Vehicle:
    # This is all GPIO Pin numbering
    pins_left = ()
    pins_right = ()
    pins_grab = ()
    pins_lift = ()

    pin_magnet = 10

    grabbing_range = 10

    steps_per_degree = 10
    steps_per_centimeter = 1000

    steps_lift = 10
    steps_grab = 10

    def __init__(self):
        self.left_wheel = ULN2003(Vehicle.pins_left)
        self.right_wheel = ULN2003(Vehicle.pins_right)
        self.grabber = ULN2003(Vehicle.pins_grab)
        self.lift = ULN2003(Vehicle.pins_lift)
        self.range_detector = RangeDetector(15, 15)
        self.magnet = Led(Vehicle.pin_magnet)

    def forward(self, steps=1000, step_size=1):
        for i in range(steps):
            self.left_wheel.step(n=step_size)
            self.right_wheel.step(n=step_size)

    def left(self, steps=90 * steps_per_degree):
        self.left_wheel.step(n=steps)

    def right(self, steps=90 * steps_per_degree):
        self.right_wheel.step(n=steps)

    def backward(self, steps=1000, step_size=1):
        self.forward(steps=-steps, step_size=step_size)

    def activate_magnet(self):
        self.magnet.activate()

    def deactivate_magnet(self):
        self.magnet.deactivate()

    def lift_up(self):
        self.lift.step(n=Vehicle.steps_lift)

    def lift_down(self):
        self.lift.step(n=-Vehicle.steps_lift)

    def grab(self):
        self.grabber.step(n=Vehicle.steps_grab)

    def free(self):
        self.grabber.step(n=-Vehicle.steps_grab)
