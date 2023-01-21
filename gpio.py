import RPi.GPIO as GPIO
import time

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Gpio(metaclass=SingletonMeta):
    def __init__(self,gpio1:int,gpio2:int) -> None:
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.gpio1, GPIO.OUT)
        GPIO.setup(self.gpio2, GPIO.OUT)

        # estudar PWM
        self.resistor = GPIO.PWM(self.gpio1,1000)
        self.ventoinha = GPIO.PWM(self.gpio2,1000)

    def hello(self):
        print("Hello from singleton class")

    def change_fan_duty(self,duty : int) -> None:
        self.ventoinha.ChangeDutyCycle(duty)
        print("Duty mudada")
    
    def change_resistor_duty(self, duty:int) -> None:
        self.resistor.ChangeDutyCycle(duty)
        print("Duty mudada")
    