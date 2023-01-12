import RPi.GPIO as GPIO

def init_gpio(gpio1:int,gpio2:int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gpio1, GPIO.OUT)
    GPIO.setup(gpio2, GPIO.OUT)
    GPIO.PWM(gpio1,1000)
    GPIO.PWM(gpio2,1000)
