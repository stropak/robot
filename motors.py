import RPi.GPIO as GPIO

""" this class allows you to control DC motors using the waveshare driver board """


class Motors:

    def __init__(self) -> None:
        # set frequency
        self.PWM_FREQUENCY = 50
        self.SPEED = 90

        # label pins
        self.MR_ACTIVATE = 26
        self.ML_ACTIVATE = 12
        self.MR_F = 21
        self.MR_B = 20
        self.ML_F = 13
        self.ML_B = 6

        # set GPIO pins as output 
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.MR_ACTIVATE, GPIO.OUT)
        GPIO.setup(self.ML_ACTIVATE, GPIO.OUT)
        GPIO.setup(self.MR_F, GPIO.OUT)
        GPIO.setup(self.MR_B, GPIO.OUT)
        GPIO.setup(self.ML_F, GPIO.OUT)
        GPIO.setup(self.ML_B, GPIO.OUT)

        # set frequency pwm frekvency of motors
        self.power_MR = GPIO.PWM(self.MR_ACTIVATE, self.PWM_FREQUENCY)
        self.power_ML = GPIO.PWM(self.ML_ACTIVATE, self.PWM_FREQUENCY)

    # move forward
    def forward(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # move backward
    def backward(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

    # turn left (on spot)
    def left(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

    # turn right (on spot)
    def right(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # brake
    def brake(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)

    # activate motors
    def start(self):
        self.power_MR.start(self.SPEED)
        self.power_ML.start(self.SPEED)

    # deactivate motors
    def stop(self):
        self.power_MR.stop()
        self.power_ML.stop()

    # change the rotation speed of the motors for both motors
    def change_speed(self, new_speed):
        self.power_MR.ChangeDutyCycle(new_speed)
        self.power_ML.ChangeDutyCycle(new_speed)

    # change the rotation speed of the motors for right motor
    def change_speed_right(self, new_speed):
        self.power_MR.ChangeDutyCycle(new_speed)

    # change the rotation speed of the motors for left motor
    def change_speed_left(self, new_speed):
        self.power_ML.ChangeDutyCycle(new_speed)

    # turn left
    def turn_left(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)

    # turn right 
    def turn_right(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # turn right while moving backward
    def turn_right_back(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

   # turn left while moving backward
    def turn_left_back(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)
