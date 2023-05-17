from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

""" the class is used to determine the distance using an ultrasonic sensor"""

class Ultrasonic:

    def __init__(self) -> None:
        FACTORY = PiGPIOFactory()
        TRIGGER_PIN = 17
        ECHO_PIN = 27

        self.sensor = DistanceSensor(trigger=TRIGGER_PIN,
                                     echo=ECHO_PIN, pin_factory=FACTORY)

    def get_distance(self):
        distance = self.sensor.value
        distance_cm = distance*100
        return distance_cm
