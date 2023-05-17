from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

""" this class is used to control servomotors for camera rotation """


# the angle by which the servo moves in one step
ANGLE = 0.08


class Servos:

    def __init__(self) -> None:
        FACTORY = PiGPIOFactory()

        # servo pins
        S_HORIZONTAL_PIN = 14
        S_VERTICAL_PIN = 15

        self.servo_horizontal = Servo(S_HORIZONTAL_PIN, pin_factory=FACTORY)
        self.servo_vertical = Servo(S_VERTICAL_PIN, pin_factory=FACTORY)

        self.servo_horizontal.value = 0
        self.servo_vertical.value = 0

    # methods for moving the camera

    def left(self):
        if (self.servo_horizontal.value < (0.9-ANGLE)):
            self.servo_horizontal.value += ANGLE

    def right(self):
        if (self.servo_horizontal.value > (-0.9+ANGLE)):
            self.servo_horizontal.value -= ANGLE

    def down(self):
        if (self.servo_vertical.value < (1-ANGLE)):
            self.servo_vertical.value += ANGLE

    def up(self):
        if (self.servo_vertical.value > (-1+ANGLE)):
            self.servo_vertical.value -= ANGLE

    def center(self):
        self.servo_horizontal.value = 0
        self.servo_vertical.value = 0

    def top(self):
        self.servo_vertical.value = 0.1
