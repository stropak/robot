import RPi.GPIO as GPIO

""" třída umožňuje ovládat stejnosměrné motory pomocí driver boardu waveshare  """


class Motors:

    def __init__(self) -> None:
        # nastaveni frekvence pwm
        self.PWM_FREQUENCY = 50
        self.SPEED = 90

        # označení pinů
        self.MR_ACTIVATE = 26
        self.ML_ACTIVATE = 12
        self.MR_F = 21
        self.MR_B = 20
        self.ML_F = 13
        self.ML_B = 6

        # Nastavení GPIO pinů jako vytsup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.MR_ACTIVATE, GPIO.OUT)
        GPIO.setup(self.ML_ACTIVATE, GPIO.OUT)
        GPIO.setup(self.MR_F, GPIO.OUT)
        GPIO.setup(self.MR_B, GPIO.OUT)
        GPIO.setup(self.ML_F, GPIO.OUT)
        GPIO.setup(self.ML_B, GPIO.OUT)

        # nastaveni pwm frekvence motoru
        self.power_MR = GPIO.PWM(self.MR_ACTIVATE, self.PWM_FREQUENCY)
        self.power_ML = GPIO.PWM(self.ML_ACTIVATE, self.PWM_FREQUENCY)

    # jízda vpřed
    def forward(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # jízda vzad
    def backward(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

    # otočení na místě směrem doleva
    def left(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

    # otočení na místě směrem doprava
    def right(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # zastavení
    def brake(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)

    # aktivace motorů
    def start(self):
        self.power_MR.start(self.SPEED)
        self.power_ML.start(self.SPEED)

    # deaktivace motorů
    def stop(self):
        self.power_MR.stop()
        self.power_ML.stop()

    # změna rychlosti otáčení motorů pro oba motory
    def change_speed(self, new_speed):
        self.power_MR.ChangeDutyCycle(new_speed)
        self.power_ML.ChangeDutyCycle(new_speed)

    # změna rychlosti otáčení peo pravý motor
    def change_speed_right(self, new_speed):
        self.power_MR.ChangeDutyCycle(new_speed)

    # změna rychlosti otáčení pro levý motor
    def change_speed_left(self, new_speed):
        self.power_ML.ChangeDutyCycle(new_speed)

    # zatočení doleva během jízdy vpřed
    def turn_left(self):
        GPIO.output(self.MR_F, 1)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)

    # zatočení doprava během jízdy vpřed
    def turn_right(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 1)
        GPIO.output(self.ML_B, 0)

    # zatočení doprava během jízdy vzad
    def turn_right_back(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 0)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 1)

   # zatočení doleva během jízdy vzad
    def turn_left_back(self):
        GPIO.output(self.MR_F, 0)
        GPIO.output(self.MR_B, 1)
        GPIO.output(self.ML_F, 0)
        GPIO.output(self.ML_B, 0)
